from scripts.validate_commit_message import validate


def test_accepts_compliant_commit_message() -> None:
    message = (
        "feat: Add task creation endpoint\n\n"
        "Create a complete vertical slice so teams can reuse a tested API\n"
        "pattern without copying product-specific code.\n"
    )

    assert validate(message) == []


def test_rejects_subject_and_body_violations() -> None:
    message = (
        "feat: Added an unnecessarily long task creation endpoint.\n"
        "Body is not separated and this line is intentionally made longer than the configured "
        "seventy-two character body limit.\n"
    )

    errors = validate(message)

    assert any("maximum is 50" in error for error in errors)
    assert "subject must not end with a period" in errors
    assert "subject and body must be separated by one blank line" in errors
    assert any("maximum is 72" in error for error in errors)


def test_requires_capitalized_imperative_description() -> None:
    assert validate("fix: fixes task lookup\n\nExplain why.\n") == [
        "description after the type must start with a capital letter"
    ]
    assert validate("fix: Fixed task lookup\n\nExplain why.\n") == [
        "subject must use imperative mood, such as 'Add' or 'Fix'"
    ]
