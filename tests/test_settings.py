import pytest
import os
from unittest.mock import patch, AsyncMock
from app.settings import Configs


@pytest.fixture
def mock_env_vars():
    os.environ["GWTDADOS_HOST"] = "test_host"
    os.environ["GWTDADOS_USERNAME"] = "test_user"
    os.environ["GWTDADOS_PASSWORD"] = "test_pass"
    yield
    del os.environ["GWTDADOS_HOST"]
    del os.environ["GWTDADOS_USERNAME"]
    del os.environ["GWTDADOS_PASSWORD"]


@pytest.mark.asyncio
@patch("app.settings.get_auth_token", new_callable=AsyncMock)
async def test_login(mock_get_auth_token, mock_env_vars):
    mock_get_auth_token.return_value = "test_token"

    configs = Configs()
    await configs.login()

    assert len(configs.auth_token) > 0
