from fastapi_starter.core.config import Settings


def test_production_disables_api_docs() -> None:
    assert Settings(env="production").expose_docs is False
    assert Settings(env="local").expose_docs is True
