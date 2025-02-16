import os
import pytest
from app.getters.register import fetch_registers_modbus, fetch_registers_dnp


# Teste da função de registers
@pytest.mark.asyncio
async def test_fetch_registers_modbus_by_sensor(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    # sensor_modbus_id = examples["valid_sensor_modbus_id"]
    sensor_modbus_id = "17BC1946-AF94-42AC-BC05-B6141C001272"
    print("sensor_modbus_id", sensor_modbus_id)
    data_registers = await fetch_registers_modbus(
        host, auth_token, sensor_modbus_id=sensor_modbus_id
    )
    assert len(data_registers) > 0


@pytest.mark.asyncio
async def test_fetch_registers_dnp_by_sensor(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    hardware_id = examples["valid_hardware_id_dnp3"]
    data_registers = await fetch_registers_dnp(
        host, auth_token, hardware_id=hardware_id
    )
    assert len(data_registers) > 0
