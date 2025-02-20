import os

import pytest

from app.getters.register import (
    fetch_register_dnp_by_id,
    fetch_register_modbus_by_id,
    fetch_registers_dnp,
    fetch_registers_modbus,
    parse_register_dnp_data,
    parse_register_modbus_data,
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
    sensor_dnp_id = examples["valid_sensor_dnp_id"]
    print("sensor_dnp_id", sensor_dnp_id)
    data_registers = await fetch_registers_dnp(
        host, auth_token, sensor_dnp_id=sensor_dnp_id
    )
    assert len(data_registers) > 0


@pytest.mark.asyncio
async def test_fetch_register_dnp_by_id(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    register_dnp_id = examples["valid_register_dnp_id"]
    print("register_dnp_id", register_dnp_id)
    data_registers = await fetch_register_dnp_by_id(
        host, auth_token, register_dnp_id=register_dnp_id
    )
    assert len(data_registers) > 0


def flatten_dict(d):
    result = []
    for v in d.values():
        if isinstance(v, dict):  # Se for um dicionário, chamar recursivamente
            result.extend(flatten_dict(v))
        elif isinstance(v, list):  # Se for uma lista, expandir os elementos
            result.extend(str(v))
        else:  # Se for valor único, apenas adicionar
            result.append(str(v))
    return result


@pytest.mark.asyncio
async def test_fetch_register_dnp_by_id(auth_token, examples):
    host = os.environ["GWTDADOS_HOST"]
    register_dnp_id = examples["valid_register_dnp_id"]
    print("register_dnp_id", register_dnp_id)
    data_registers = await fetch_register_dnp_by_id(
        host, auth_token, register_dnp_id=register_dnp_id
    )
    assert len(data_registers) > 0


# @pytest.mark.asyncio
# async def test_parse_register_dnp_data(auth_token, examples):
#     host = os.environ["GWTDADOS_HOST"]
#     register_dnp_id = examples["valid_register_dnp_id"]
#     data_register = await fetch_register_dnp_by_id(
#         host, auth_token, register_dnp_id=register_dnp_id
#     )
#     parsed_register = parse_register_dnp_data(data_register)
#     print("data_register:", data_register)
#     v1 = flatten_dict(data_register)
#     v1.sort()
#     print("\n\nv1", v1)
#     v2 = flatten_dict(parsed_register)
#     v2.sort()
#     print("v2", v2)
#     assert v1 == v2


# @pytest.mark.asyncio
# async def test_parse_register_modbus_data(auth_token, examples):
#     host = os.environ["GWTDADOS_HOST"]
#     register_dnp_id = examples["valid_register_modbus_id"]
#     data_register = await fetch_register_modbus_by_id(
#         host, auth_token, register_modbus_id=register_dnp_id
#     )
#     parsed_register = parse_register_modbus_data(data_register)
#     print("data_register:", data_register)
#     v1 = flatten_dict(data_register)
#     v1.sort()
#     print("\n\nv1", v1)
#     v2 = flatten_dict(parsed_register)
#     v2.sort()
#     print("\nv2", v2)
#     print("\n\n", parsed_register)
#     assert v1 == v2
