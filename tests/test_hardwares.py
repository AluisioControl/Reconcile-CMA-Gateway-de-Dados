import asyncio
import os

import pytest

from app.getters.gateway import fetch_all_gateways, fetch_gateway_by_id
from app.getters.hardware import fetch_hardware_by_id, fetch_hardwares_by_gateway
from app.login import get_auth_token


# Teste da função de hardware
@pytest.mark.asyncio
async def test_fetch_hardwares_by_gateway(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    cma_gateway_id = examples["valid_gateway_id"]
    hardwares = await fetch_hardwares_by_gateway(
        host, auth_token, cma_gateway_id=cma_gateway_id
    )
    assert len(hardwares) > 0


# Teste da função de hardware
@pytest.mark.asyncio
async def test_fetch_hardware_by_id(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    hardware_id = examples["valid_hardware_id"]
    hardwares = await fetch_hardware_by_id(host, auth_token, hardware_id=hardware_id)
    assert len(hardwares) > 0
