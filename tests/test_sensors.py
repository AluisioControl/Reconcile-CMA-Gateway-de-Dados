import os
import pytest
from app.getters.sensors import (
    fetch_sensors_modbus,
    fetch_sensors_dnp,
    fetch_sensor_modbus_by_id,
    fetch_sensor_dnp_by_id,
)


# Teste da função de hardware
@pytest.mark.asyncio
async def test_fetch_sensors_modbus(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    hardware_id = examples["valid_hardware_id"]
    data_sensors = await fetch_sensors_modbus(host, auth_token, hardware_id=hardware_id)
    print(data_sensors)
    assert len(data_sensors) > 0


@pytest.mark.asyncio
async def test_fetch_sensors_dnp(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    hardware_id = examples["valid_hardware_id_dnp3"]
    data_sensors = await fetch_sensors_dnp(host, auth_token, hardware_id=hardware_id)
    print("sensor dnp3", data_sensors)
    assert len(data_sensors) > 0


@pytest.mark.asyncio
async def test_fetch_sensor_modbus_by_id(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    hardware_id = examples["valid_hardware_id"]
    sensor_id = examples["valid_sensor_id"]
    data_sensor = await fetch_sensor_modbus_by_id(
        host, auth_token, sensor_id=hardware_id, sensor_id=sensor_id
    )
    print(data_sensor)
    assert data_sensor is not None


@pytest.mark.asyncio
async def test_fetch_sensor_dnp_by_id(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    hardware_id = examples["valid_hardware_id_dnp3"]
    sensor_id = examples["valid_sensor_id_dnp3"]
    data_sensor = await fetch_sensor_dnp_by_id(
        host, auth_token, hardware_id=hardware_id, sensor_id=sensor_id
    )
    print("sensor dnp3 by id", data_sensor)
    assert data_sensor is not None
