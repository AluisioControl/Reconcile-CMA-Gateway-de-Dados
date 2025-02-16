from abc import ABC, abstractmethod
from .login import get_auth_token
from app.getters.gateway import fetch_all_gateways, fetch_gateway_by_id, parse_gateway_data
from app.getters.hardware import fetch_hardwares_by_gateway, fetch_hardware_by_id, parse_hardware_data
from app.getters.sensors import fetch_sensors_modbus, fetch_sensor_modbus_by_id, parse_sensor_modbus_data

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

def combine_primary_with_secondary(primary: dict, secondary_list: list[dict]) -> list[dict]:
    """
    Combina o dicionário primário com cada dicionário da lista secundária.
    
    :param primary: Dicionário com informações primárias.
    :param secondary_list: Lista de dicionários com informações secundárias.
    :return: Lista de dicionários combinados.
    """
    return [{**primary, **secondary} for secondary in secondary_list]

async def main():
    all_flat_data = []
    hardwares_parsed = []
    sensors_parsed = []
    gateways = await fetch_all_gateways(host=configs.host, auth_token=configs.auth_token)
    for gateway in gateways:
        gateway_id = gateway["id"]
        gateway_data = await fetch_gateway_by_id(host=configs.host, auth_token=configs.auth_token, gateway_id=gateway_id)
        gateway_parsed = parse_gateway_data(gateway_data)
        print("gateway parsed:", gateway_parsed)
        for hardware in await fetch_hardwares_by_gateway(host=configs.host, auth_token=configs.auth_token, cma_gateway_id=gateway_id):
            hardware_id = hardware["id"]
            hardware_data = await fetch_hardware_by_id(host=configs.host, auth_token=configs.auth_token, hardware_id=hardware_id)
            hardware_parsed = parse_hardware_data(hardware_data)
            print("hardware parsed:", hardware_parsed)
            hardwares_parsed.append(hardware_parsed)
            # consultar todos os sensor MODBUS associado a cada hardware
            sensors_parsed = []
            sensors = await fetch_sensors_modbus(host=configs.host, auth_token=configs.auth_token, hardware_id=hardware_id)
            print("\n\n\n")
            print("sensors:", sensors)
            if not sensors["content"]:
                sensors_parsed.append(parse_sensor_modbus_data({}))
            else:
                for sensor in sensors["content"]: # informação de sensores modbus paginada
                    print("sensor modbus:", sensor)
                    sensor_id = sensor["id"]
                    sensor_data = await fetch_sensor_modbus_by_id(host=configs.host, auth_token=configs.auth_token, sensor_modbus_id=sensor_id)
                    sensor_parsed = parse_sensor_modbus_data(sensor_data)
                    sensors_parsed.append(sensor_parsed)
                    print("sensor modbus:", sensor)
            print("hardware_parsed:", hardware_parsed)
            print("sensors parsed:", sensors_parsed)
            hardware_combine_sensors_modbus = combine_primary_with_secondary(hardware_parsed, sensors_parsed)
            print("hardware_combine_sensors_modbus:", hardware_combine_sensors_modbus)
            print("\n")
        print("gateway parsed:", gateway_parsed)
        print("hardware_combine_sensors_modbus", hardware_combine_sensors_modbus)
        print("\n")
        all_flat_data += combine_primary_with_secondary(gateway_parsed, hardware_combine_sensors_modbus)
    print("all flat data:", all_flat_data)
    print("\n")
    with open("data.json", "w") as f:
        json.dump(all_flat_data, f)


if __name__ == "__main__":
    asyncio.run(main())
