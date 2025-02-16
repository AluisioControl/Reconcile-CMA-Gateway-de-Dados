import os
import pytest
from app.getters.register import (
    fetch_registers_modbus,
    fetch_register_modbus_by_id,
    fetch_registers_dnp,
    fetch_register_dnp_by_id,
)


# Teste da função de registers
@pytest.mark.asyncio
async def test_fetch_registers_modbus_by_sensor(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    sensor_modbus_id = examples["valid_sensor_modbus_id"]
    data_registers = await fetch_registers_modbus(
        host, auth_token, sensor_modbus_id=sensor_modbus_id
    )
    assert len(data_registers) > 0


@pytest.mark.asyncio
async def test_fetch_register_modbus_by_id(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    register_modbus_id = examples["valid_register_modbus_id"]
    print("register_modbus_id", register_modbus_id)
    data_registers = await fetch_register_modbus_by_id(
        host, auth_token, register_modbus_id=register_modbus_id
    )
    assert len(data_registers) > 0


@pytest.mark.asyncio
async def test_fetch_registers_dnp_by_sensor(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    sensor_dnp_id = examples["valid_sensor_dnp3_id"]
    print("sensor_dnp3_id", sensor_dnp_id)
    data_registers = await fetch_registers_dnp(
        host, auth_token, sensor_dnp_id=sensor_dnp_id
    )
    assert len(data_registers) > 0


@pytest.mark.asyncio
async def test_fetch_register_dnp_by_id(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    register_dnp_id = examples["valid_register_dnp3_id"]
    print("register_dnp_id", register_dnp_id)
    data_registers = await fetch_register_dnp_by_id(
        host, auth_token, register_dnp_id=register_dnp_id
    )
    assert len(data_registers) > 0
