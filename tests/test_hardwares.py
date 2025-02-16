import os
import pytest
import asyncio
from app.getters.gateways import fetch_all_gateways, fetch_gateway_by_id
from app.getters.hardware import fetch_hardwares_by_gateway
from app.login import get_auth_token


# Teste da função de hardware 
@pytest.mark.asyncio
async def test_fetch_hardwares_by_gateway(auth_token, examples):
    host = os.environ['GWTDADOS_HOST']
    cma_gateway_id = examples['valid_gateway_id']
    hardwares = await fetch_hardwares_by_gateway(host, auth_token, cma_gateway_id=cma_gateway_id)
    assert len(hardwares) > 0

