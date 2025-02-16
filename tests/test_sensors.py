import os
import pytest
from app.getters.sensors import fetch_sensors_modbus, fetch_sensors_dnp


# Teste da função de hardware 
@pytest.mark.asyncio
async def test_fetch_sensors_modbus(auth_token, examples):
    host = os.environ['GWTDADOS_HOST']
    hardware_id = examples['valid_hardware_id']
    data_sensors = await fetch_sensors_modbus(host, auth_token, hardware_id=hardware_id)
    assert len(data_sensors) > 0


@pytest.mark.asyncio
async def test_fetch_sensors_dnp(auth_token, examples):
    host = os.environ['GWTDADOS_HOST']
    hardware_id = examples['valid_hardware_id_dnp3']
    data_sensors = await fetch_sensors_dnp(host, auth_token, hardware_id=hardware_id)
    assert len(data_sensors) > 0

