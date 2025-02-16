import os
import pytest
import asyncio
from app.getters.gateway import fetch_all_gateways, fetch_gateway_by_id
from app.getters.hardware import fetch_hardwares_by_gateway
from app.login import get_auth_token


# Teste da função de obtenção do token
@pytest.mark.asyncio
async def test_get_auth_token():
    host = os.environ["GWTDADOS_HOST"]
    username = os.environ["GWTDADOS_USERNAME"]
    password = os.environ["GWTDADOS_PASSWORD"]

    try:
        token = await get_auth_token(host, username, password)
        assert token is not None  # Verifica se o token foi gerado com sucesso
        print(f"Received token: {token}")
    except Exception as e:
        pytest.fail(f"Error: {e}")


# Teste da função de fetch de todos os gateways
@pytest.mark.asyncio
async def test_fetch_all_gateways(auth_token):
    host = os.environ["GWTDADOS_HOST"]
    gateways = await fetch_all_gateways(host, auth_token)
    assert len(gateways) > 0


# Teste da função de fetch de gateway específico
@pytest.mark.asyncio
async def test_fetch_gateway_by_id(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]

    # gateway_id = "56B742EF-AED1-EF11-88F9-6045BDFE79DC"  # Substitua pelo ID do gateway desejado
    gateway_id = examples["valid_gateway_id"]

    try:
        gateway_info = await fetch_gateway_by_id(host, auth_token, gateway_id)
        assert (
            "id" in gateway_info
        )  # Verifica se o ID está presente na resposta do gateway
        print(f"Gateway Info [{gateway_id}]: {gateway_info}")
    except Exception as e:
        pytest.fail(f"Error: {e}")
