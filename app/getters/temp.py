from abc import ABC, abstractmethod
from .login import get_auth_token
from app.getters.gateway import (
    fetch_all_gateways,
    fetch_gateway_by_id,
    parse_gateway_data,
)
from app.getters.hardware import (
    fetch_hardwares_by_gateway,
    fetch_hardware_by_id,
    parse_hardware_data,
)
from app.getters.sensors import (
    fetch_sensors_modbus,
    fetch_sensor_modbus_by_id,
    parse_sensor_modbus_data,
    parse_sensor_dnp_data,
    fetch_sensors_dnp,
    fetch_sensor_dnp_by_id,
)
from app.getters.register import (
    fetch_register_modbus_by_id,
    fetch_registers_modbus,
    parse_register_modbus_data,
    fetch_register_dnp_by_id,
    fetch_registers_dnp,
    parse_register_dnp_data
)


import os
from .settings import configs
import asyncio

import json


def multiplex_dicts(primary_list: list[dict], secondary_list: list[dict]) -> list[dict]:
    """
    Combina cada dicionário da lista primária com cada dicionário da lista secundária.

    :param primary_list: Lista de dicionários com informações primárias.
    :param secondary_list: Lista de dicionários com informações secundárias.
    :return: Lista de dicionários combinados.
    """
    # Usa compreensão de listas para fundir cada par com desempacotamento de dicionários
    return [{**p, **s} for p in primary_list for s in secondary_list]


def combine_primary_with_secondary(
    primary: dict, secondary_list: list[dict]
) -> list[dict]:
    """
    Combina o dicionário primário com cada dicionário da lista secundária.

    :param primary: Dicionário com informações primárias.
    :param secondary_list: Lista de dicionários com informações secundárias.
    :return: Lista de dicionários combinados.
    """
    return [{**primary, **secondary} for secondary in secondary_list]

DEBUG=False

async def collect_registers_modbus(sensor_modbus_id):
    registers = []
    print("sensor_modbus_id", sensor_modbus_id)
    registers_data = await fetch_registers_modbus(
        host=configs.host, auth_token=configs.auth_token, sensor_modbus_id=sensor_modbus_id)
    print("registers_data", registers_data)
    for register_data in registers_data["content"]:
        print("\t\t\tregister_data", register_data)
        register_data = await fetch_register_modbus_by_id(
            host=configs.host, auth_token=configs.auth_token, register_modbus_id=register_data["id"])
        register_parsed = parse_register_modbus_data(register_data)
        registers.append(register_parsed)
        if DEBUG: break
    print(registers)
    return registers


async def collect_registers_dnp(sensor_dnp_id):
    registers = []
    print("sensor_dnp_id", sensor_dnp_id)
    registers_data = await fetch_registers_dnp(
        host=configs.host, auth_token=configs.auth_token, sensor_dnp_id=sensor_dnp_id)
    print("registers_data", registers_data)

    async def fetch_and_parse_register(register_data):
        print("\tregister_data", register_data)
        register_data = await fetch_register_dnp_by_id(
            host=configs.host, auth_token=configs.auth_token, register_dnp_id=register_data["id"])
        return parse_register_dnp_data(register_data)

    tasks = [fetch_and_parse_register(register_data) for register_data in registers_data["content"]]
    registers = await asyncio.gather(*tasks)
    
    print(registers)
    return registers


async def main():
    all_flat_data = []
    hardwares_parsed = []
    sensors_parsed = []
    gateways = await fetch_all_gateways(
        host=configs.host, auth_token=configs.auth_token
    )
    for gateway in gateways:
        gateway_id = gateway["id"]
        print("gateway_id:", gateway_id)
        gateway_data = await fetch_gateway_by_id(
            host=configs.host, auth_token=configs.auth_token, gateway_id=gateway_id
        )
        gateway_parsed = parse_gateway_data(gateway_data)
        hardware_combine_sensors_modbus = []
        hardware_combine_sensors_dnp = []
        for hardware in await fetch_hardwares_by_gateway(
            host=configs.host, auth_token=configs.auth_token, cma_gateway_id=gateway_id
        ):
            hardware_id = hardware["id"]
            print("\t hardware_id", hardware_id)
            hardware_data = await fetch_hardware_by_id(
                host=configs.host,
                auth_token=configs.auth_token,
                hardware_id=hardware_id,
            )
            hardware_parsed = parse_hardware_data(hardware_data)
            hardwares_parsed.append(hardware_parsed)

            # consultar todos os sensor MODBUS associado a cada hardware
            sensors_parsed = []
            sensors = await fetch_sensors_modbus(
                host=configs.host,
                auth_token=configs.auth_token,
                hardware_id=hardware_id,
            )
            if not sensors["content"]:
                # sensors_parsed.append(parse_sensor_modbus_data({})) # adicionar um sensor vazio
                print("\t\t sensor_modbus_id", "null")
            else:
                for sensor in sensors[
                    "content"
                ]:  # informação de sensores modbus paginada
                    sensor_id = sensor["id"]
                    print("\t\t sensor_modbus_id", sensor_id)
                    sensor_data = await fetch_sensor_modbus_by_id(
                        host=configs.host,
                        auth_token=configs.auth_token,
                        sensor_modbus_id=sensor_id,
                    )
                    sensor_parsed = parse_sensor_modbus_data(sensor_data)
                    sensors_parsed.append(sensor_parsed)
                    # coletar os registros de cada sensor
                    registers_modbus = await collect_registers_modbus(sensor_id)
                    sensor_combine_registers_modbus =combine_primary_with_secondary(sensor_parsed, registers_modbus)
                    if DEBUG: break
            # combinar o resultado de hardware com o resultado de sensores
            hardware_combine_sensors_modbus += combine_primary_with_secondary(
                hardware_parsed, sensor_combine_registers_modbus
            )

            # consultar todos os sensor DNP associado a cada hardware
            sensors_dnp_parsed = []
            sensors_dnp = await fetch_sensors_dnp(
                host=configs.host,
                auth_token=configs.auth_token,
                active=True,
                hardware_id=hardware_id,
            )
            if not sensors_dnp["content"]:
                # sensors_dnp_parsed.append(parse_sensor_dnp_data({})) # adicionar um sensor vazio
                print("\t\t sensor_dnp_id", "null")
            else:
                for sensor_dnp in sensors_dnp[
                    "content"
                ]:  # informação de sensores modbus paginada
                    sensor_dnp_id = sensor_dnp["id"]
                    print("\t\t sensor_dnp_id", sensor_dnp_id)
                    try:
                        sensor_dnp_data = await fetch_sensor_dnp_by_id(
                            host=configs.host,
                            auth_token=configs.auth_token,
                            sensor_dnp_id=sensor_dnp_id,
                        )
                        sensor_dnp_parsed = parse_sensor_dnp_data(sensor_dnp_data)
                        sensors_dnp_parsed.append(sensor_dnp_parsed)
                        sensors_parsed.append(sensor_parsed)
                    except Exception as e:
                        print("\t\t sensor_dnp ERROR!!!")
                        print("\t\t   sensor_dnp_id", sensor_dnp_id)
                        print("\t\t   ", e)
                        pass
                    if DEBUG: break
            # combinar o resultado de hardware com o resultado de sensores
            hardware_combine_sensors_dnp += combine_primary_with_secondary(
                hardware_parsed, sensors_dnp_parsed
            )
            if DEBUG: break
        all_flat_data += combine_primary_with_secondary(
            gateway_parsed, hardware_combine_sensors_modbus
        )
        all_flat_data += combine_primary_with_secondary(
            gateway_parsed, hardware_combine_sensors_dnp
        )
    # Salvar os dados em um arquivo JSON
    with open("data.json", "w") as f:
        json.dump(all_flat_data, f)


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(collect_registers_modbus(sensor_modbus_id="17BC1946-AF94-42AC-BC05-B6141C001272"))
    # asyncio.run(collect_registers_dnp(sensor_dnp_id="AF345D34-0DEC-EF11-88FB-6045BDFE79DC"))