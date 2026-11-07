#!/usr/bin/env bash

set -uo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)"

TARGET_CLAUDE=0
TARGET_CODEX=0
CHECK_ONLY=0
ASSUME_YES=0
ISSUES=0

SUPERPOWERS_CLAUDE="superpowers@claude-plugins-official"
PONYTAIL_MARKETPLACE="DietrichGebert/ponytail"
PONYTAIL_PLUGIN="ponytail@ponytail"

usage() {
  cat <<'EOF'
Usage: ./scripts/setup_agent_tools.sh [options]

Check and optionally install the agent tools used by this repository.

Options:
  --claude   Configure Claude Code
  --codex    Configure Codex CLI and Codex app plugins
  --all      Configure both Claude Code and Codex
  --check    Report status without installing or changing configuration
  --yes      Accept supported installation prompts non-interactively
  -h, --help Show this help

With no options, the script opens an interactive target menu. Repository-local
skills already work without global plugins; this script installs their full
upstream versions and configures CodeGraph.
EOF
}

ok() {
  printf '[ok] %s\n' "$1"
}

warn() {
  printf '[warning] %s\n' "$1"
}

note() {
  printf '[info] %s\n' "$1"
}

confirm() {
  local prompt="$1"
  local answer

  if [[ "${ASSUME_YES}" -eq 1 ]]; then
    return 0
  fi
  if [[ ! -t 0 ]]; then
    return 1
  fi

  read -r -p "${prompt} [y/N] " answer
  [[ "${answer}" == "y" || "${answer}" == "Y" ]]
}

run_step() {
  local label="$1"
  shift

  note "${label}"
  printf '       $'
  printf ' %q' "$@"
  printf '\n'
  if "$@"; then
    return 0
  fi

  warn "${label} failed"
  return 1
}

contains_text() {
  local content="$1"
  local expected="$2"
  printf '%s' "${content}" | grep -Fqi -- "${expected}"
}

claude_plugins() {
  claude plugin list --json 2>/dev/null
}

codex_plugins() {
  codex plugin list --json 2>/dev/null || codex plugin list 2>/dev/null
}

codegraph_configured_for() {
  local target="$1"
  local codex_home="${CODEX_HOME:-${HOME}/.codex}"
  local file
  local -a files=()

  if [[ "${target}" == "claude" ]]; then
    files=("${HOME}/.claude.json" "${PROJECT_ROOT}/.mcp.json")
  else
    files=("${codex_home}/config.toml" "${PROJECT_ROOT}/.codex/config.toml")
  fi

  for file in "${files[@]}"; do
    if [[ -f "${file}" ]] && grep -Fqi 'codegraph' "${file}"; then
      return 0
    fi
  done
  return 1
}

install_claude_plugins() {
  local plugins
  local marketplaces

  if ! command -v claude >/dev/null 2>&1; then
    return
  fi
  plugins="$(claude_plugins || true)"

  if ! contains_text "${plugins}" 'superpowers'; then
    warn "Superpowers is not installed for Claude Code"
    if confirm "Install ${SUPERPOWERS_CLAUDE} for Claude Code?"; then
      run_step "Installing Superpowers for Claude Code" \
        claude plugin install --scope user "${SUPERPOWERS_CLAUDE}" || true
    fi
  fi

  if ! contains_text "${plugins}" 'ponytail'; then
    warn "Ponytail is not installed for Claude Code"
    if confirm "Install ${PONYTAIL_PLUGIN} for Claude Code?"; then
      marketplaces="$(claude plugin marketplace list --json 2>/dev/null || true)"
      if ! contains_text "${marketplaces}" 'DietrichGebert/ponytail' && \
         ! contains_text "${marketplaces}" '"name": "ponytail"'; then
        run_step "Adding the Ponytail marketplace to Claude Code" \
          claude plugin marketplace add --scope user "${PONYTAIL_MARKETPLACE}" || return
      fi
      run_step "Installing Ponytail for Claude Code" \
        claude plugin install --scope user "${PONYTAIL_PLUGIN}" || true
    fi
  fi
}

install_codex_plugins() {
  local plugins

  if ! command -v codex >/dev/null 2>&1; then
    return
  fi
  plugins="$(codex_plugins || true)"

  if ! contains_text "${plugins}" 'ponytail'; then
    warn "Ponytail is not installed for Codex"
    if confirm "Install ${PONYTAIL_PLUGIN} for Codex?"; then
      run_step "Adding the Ponytail marketplace to Codex" \
        codex plugin marketplace add "${PONYTAIL_MARKETPLACE}" || return
      run_step "Installing Ponytail for Codex" \
        codex plugin add "${PONYTAIL_PLUGIN}" || true
    fi
  fi

  if ! contains_text "${plugins}" 'superpowers'; then
    warn "Superpowers requires the Codex plugin browser"
    note "Open Codex, run /plugins, search for Superpowers, and select Install Plugin."
  fi
}

install_codegraph() {
  local targets=""
  local needs_config=0

  if [[ "${TARGET_CLAUDE}" -eq 1 ]]; then
    targets="claude"
    codegraph_configured_for claude || needs_config=1
  fi
  if [[ "${TARGET_CODEX}" -eq 1 ]]; then
    targets="${targets:+${targets},}codex"
    codegraph_configured_for codex || needs_config=1
  fi

  if ! command -v codegraph >/dev/null 2>&1; then
    warn "CodeGraph CLI is not installed"
    if command -v npx >/dev/null 2>&1 && \
       confirm "Install CodeGraph and configure ${targets}?"; then
      run_step "Installing CodeGraph" \
        npx -y @colbymchenry/codegraph install \
        --target="${targets}" --location=global --yes || true
      hash -r
    else
      note "Official installer: npx @colbymchenry/codegraph"
    fi
  elif [[ "${needs_config}" -eq 1 ]] && \
       confirm "Configure CodeGraph for ${targets}?"; then
    run_step "Configuring CodeGraph" \
      codegraph install --target="${targets}" --location=global --yes || true
  fi

  if command -v codegraph >/dev/null 2>&1 && \
     ! codegraph status "${PROJECT_ROOT}" --json >/dev/null 2>&1; then
    warn "The repository does not have a usable CodeGraph index"
    if confirm "Initialize CodeGraph for this repository?"; then
      run_step "Initializing the repository CodeGraph index" \
        codegraph init --yes "${PROJECT_ROOT}" || true
    fi
  fi
}

verify_bundled_skills() {
  local skill
  for skill in superpowers-workflow ponytail codegraph-first loadless-engineering-developer; do
    if [[ -f "${PROJECT_ROOT}/.agents/skills/${skill}/SKILL.md" ]]; then
      ok "Repository skill: ${skill}"
    else
      warn "Repository skill is missing: ${skill}"
      ISSUES=$((ISSUES + 1))
    fi
  done
}

verify_node() {
  if command -v node >/dev/null 2>&1; then
    ok "Node.js: $(node --version 2>/dev/null || printf 'installed')"
  else
    warn "Node.js is missing; Ponytail hooks will not run"
    ISSUES=$((ISSUES + 1))
  fi
}

verify_claude() {
  local plugins

  if ! command -v claude >/dev/null 2>&1; then
    warn "Claude Code CLI: missing"
    ISSUES=$((ISSUES + 1))
    return
  fi
  ok "Claude Code CLI: $(claude --version 2>/dev/null || printf 'installed')"
  plugins="$(claude_plugins || true)"

  if contains_text "${plugins}" 'superpowers'; then
    ok "Claude Code plugin: Superpowers"
  else
    warn "Claude Code plugin missing: Superpowers"
    ISSUES=$((ISSUES + 1))
  fi
  if contains_text "${plugins}" 'ponytail'; then
    ok "Claude Code plugin: Ponytail"
  else
    warn "Claude Code plugin missing: Ponytail"
    ISSUES=$((ISSUES + 1))
  fi
  if codegraph_configured_for claude; then
    ok "Claude Code integration: CodeGraph"
  else
    warn "Claude Code integration missing: CodeGraph"
    ISSUES=$((ISSUES + 1))
  fi
}

verify_codex() {
  local plugins

  if ! command -v codex >/dev/null 2>&1; then
    warn "Codex CLI: missing; Codex app plugins cannot be verified from this shell"
    note "In the Codex app, install Superpowers from Plugins."
    note "For Ponytail, install the Codex CLI and rerun this script."
    ISSUES=$((ISSUES + 1))
  else
    ok "Codex CLI: $(codex --version 2>/dev/null || printf 'installed')"
    plugins="$(codex_plugins || true)"
    if contains_text "${plugins}" 'superpowers'; then
      ok "Codex plugin: Superpowers"
    else
      warn "Codex plugin missing: Superpowers"
      note "Run /plugins in Codex, search for Superpowers, and install it."
      ISSUES=$((ISSUES + 1))
    fi
    if contains_text "${plugins}" 'ponytail'; then
      ok "Codex plugin: Ponytail"
    else
      warn "Codex plugin missing: Ponytail"
      ISSUES=$((ISSUES + 1))
    fi
  fi

  if codegraph_configured_for codex; then
    ok "Codex integration: CodeGraph"
  else
    warn "Codex integration missing: CodeGraph"
    ISSUES=$((ISSUES + 1))
  fi
}

verify_codegraph_project() {
  if ! command -v codegraph >/dev/null 2>&1; then
    warn "CodeGraph CLI: missing"
    ISSUES=$((ISSUES + 1))
    return
  fi
  ok "CodeGraph CLI: $(codegraph --version 2>/dev/null || printf 'installed')"
  if codegraph status "${PROJECT_ROOT}" --json >/dev/null 2>&1; then
    ok "CodeGraph project index: ready"
  else
    warn "CodeGraph project index: missing or stale"
    ISSUES=$((ISSUES + 1))
  fi
}

select_targets() {
  local choice

  if [[ "${TARGET_CLAUDE}" -eq 1 || "${TARGET_CODEX}" -eq 1 ]]; then
    return
  fi
  if [[ "${CHECK_ONLY}" -eq 1 || "${ASSUME_YES}" -eq 1 || ! -t 0 ]]; then
    TARGET_CLAUDE=1
    TARGET_CODEX=1
    return
  fi

  printf '%s\n' 'Choose an agent setup:'
  printf '%s\n' '  1) Claude Code and Codex (recommended)'
  printf '%s\n' '  2) Claude Code only'
  printf '%s\n' '  3) Codex only'
  printf '%s\n' '  4) Check both without installing'
  read -r -p 'Selection [1]: ' choice
  case "${choice:-1}" in
    1) TARGET_CLAUDE=1; TARGET_CODEX=1 ;;
    2) TARGET_CLAUDE=1 ;;
    3) TARGET_CODEX=1 ;;
    4) TARGET_CLAUDE=1; TARGET_CODEX=1; CHECK_ONLY=1 ;;
    *) warn "Unknown selection: ${choice}"; exit 2 ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --claude) TARGET_CLAUDE=1 ;;
    --codex) TARGET_CODEX=1 ;;
    --all) TARGET_CLAUDE=1; TARGET_CODEX=1 ;;
    --check) CHECK_ONLY=1 ;;
    --yes) ASSUME_YES=1 ;;
    -h|--help) usage; exit 0 ;;
    *) warn "Unknown option: $1"; usage; exit 2 ;;
  esac
  shift
done

select_targets
if [[ ! -t 0 && "${ASSUME_YES}" -eq 0 ]]; then
  CHECK_ONLY=1
fi

printf '%s\n' 'Agent tool setup'
printf '%s\n' '================'
note "Repository: ${PROJECT_ROOT}"

if [[ "${CHECK_ONLY}" -eq 0 ]]; then
  [[ "${TARGET_CLAUDE}" -eq 1 ]] && install_claude_plugins
  [[ "${TARGET_CODEX}" -eq 1 ]] && install_codex_plugins
  install_codegraph
fi

printf '\n%s\n' 'Status'
printf '%s\n' '------'
verify_bundled_skills
verify_node
[[ "${TARGET_CLAUDE}" -eq 1 ]] && verify_claude
[[ "${TARGET_CODEX}" -eq 1 ]] && verify_codex
verify_codegraph_project

if [[ "${ISSUES}" -gt 0 ]]; then
  printf '\n'
  warn "Setup is incomplete: ${ISSUES} item(s) need attention"
  exit 1
fi

printf '\n'
ok 'Agent tools are ready. Restart Claude Code and Codex before using new plugins.'
