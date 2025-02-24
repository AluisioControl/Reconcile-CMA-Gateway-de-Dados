import asyncio
import json
import os
import sqlite3
from asyncio import Semaphore

import pandas as pd

from app.getters.gateway import (
    fetch_all_gateways,
    fetch_gateway_by_id,
    parse_gateway_data,
)
from app.getters.hardware import (
    fetch_hardware_by_id,
    fetch_hardwares_by_gateway,
    parse_hardware_data,
)
from app.getters.register import (
    fetch_register_dnp_by_id,
    fetch_register_modbus_by_id,
    fetch_registers_dnp,
    fetch_registers_modbus,
    parse_register_dnp_data,
    parse_register_modbus_data,
)
from app.getters.sensors import (
    fetch_sensor_dnp_by_id,
    fetch_sensor_modbus_by_id,
    fetch_sensors_dnp,
    fetch_sensors_modbus,
    parse_sensor_dnp_data,
    parse_sensor_modbus_data,
)
from app.utils.data import combine_primary_with_secondary

from .settings import configs

DEBUG = False
MAX_PAGE_SIZE = 999
semaphore = Semaphore(90)


async def fetch_and_parse_register_modbus(register_data):
    async with semaphore:
        register_data = await fetch_register_modbus_by_id(
            host=configs.host,
            auth_token=configs.auth_token,
            register_modbus_id=register_data["id"],
        )
        return parse_register_modbus_data(register_data)


async def collect_registers_modbus(sensor_modbus_id):
    registers = []
    registers_data = await fetch_registers_modbus(
        host=configs.host,
        auth_token=configs.auth_token,
        sensor_modbus_id=sensor_modbus_id,
        size=MAX_PAGE_SIZE,
    )
    # processar os registros em paralelo
    tasks = [
        fetch_and_parse_register_modbus(register_data)
        for register_data in registers_data["content"]
    ]
    print("\t\t - Coletando ", len(tasks), " registros")
    registers = await asyncio.gather(*tasks)
    return registers


async def fetch_and_parse_register_dnp(register_data):
    async with semaphore:
        register_data = await fetch_register_dnp_by_id(
            host=configs.host,
            auth_token=configs.auth_token,
            register_dnp_id=register_data["id"],
        )
    return parse_register_dnp_data(register_data)


async def collect_registers_dnp(sensor_dnp_id):
    registers = []
    registers_data = await fetch_registers_dnp(
        host=configs.host,
        auth_token=configs.auth_token,
        sensor_dnp_id=sensor_dnp_id,
        size=MAX_PAGE_SIZE,
    )
    # processar os registros em paralelo
    tasks = [
        fetch_and_parse_register_dnp(register_data)
        for register_data in registers_data["content"]
    ]
    print("\t\t\t - Coletando ", len(tasks), " registros")
    registers = await asyncio.gather(*tasks)
    return registers


async def main():
    # Acumuladores
    list_gateways = []
    list_hardwares = []
    list_sensors_modbus = []
    list_registers_modbus = []
    list_sensors_dnp3 = []
    list_registers_dnp3 = []

    all_flat_data = []
    hardwares_parsed = []
    hardwares_combined = []
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
        list_gateways.append(gateway_data)
        gateway_parsed = parse_gateway_data(gateway_data)
        hardware_combine_sensors_modbus = []
        hardware_combine_sensors_dnp = []
        hardwares = await fetch_hardwares_by_gateway(
            host=configs.host, auth_token=configs.auth_token, cma_gateway_id=gateway_id
        )
        for hardware in hardwares:
            hardware_id = hardware["id"]
            print("\t hardware_id", hardware_id)
            hardware_data = await fetch_hardware_by_id(
                host=configs.host,
                auth_token=configs.auth_token,
                hardware_id=hardware_id,
            )
            list_hardwares.append(hardware_data)
            hardware_parsed = parse_hardware_data(hardware_data)
            # hardwares_parsed.append(hardware_parsed)

            # consultar todos os sensor MODBUS associado a cada hardware
            sensors_parsed = []
            sensors = await fetch_sensors_modbus(
                host=configs.host,
                auth_token=configs.auth_token,
                hardware_id=hardware_id,
            )
            sensor_combine_registers_modbus = []
            if not sensors["content"]:
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
                    list_sensors_modbus.append(sensor_data)
                    sensor_parsed = parse_sensor_modbus_data(sensor_data)
                    sensors_parsed.append(sensor_parsed)
                    # coletar os registros de cada sensor
                    registers_modbus = await collect_registers_modbus(sensor_id)
                    list_registers_modbus += registers_modbus
                    sensor_combine_registers_modbus += combine_primary_with_secondary(
                        sensor_parsed, registers_modbus
                    )
                    print(
                        "\t\t +sub total resistros por sensor:",
                        len(sensor_combine_registers_modbus),
                    )
                    if DEBUG:
                        break
            # combinar o resultado de hardware com o resultado de sensores
            hardware_combine_sensors_modbus += combine_primary_with_secondary(
                hardware_parsed, sensor_combine_registers_modbus
            )
            print(
                "\t\t +subtotal de restristros por hardware:",
                len(hardware_combine_sensors_modbus),
            )
            # hardwares_combined += hardware_combine_sensors_modbus

            # consultar todos os sensor DNP associado a cada hardware
            sensors_dnp_parsed = []
            sensors_dnp = await fetch_sensors_dnp(
                host=configs.host,
                auth_token=configs.auth_token,
                active=True,
                hardware_id=hardware_id,
            )
            sensor_combine_registers_dnp = []
            if not sensors_dnp["content"]:
                # sensors_dnp_parsed.append(parse_sensor_dnp_data({})) # adicionar um sensor vazio
                print("\t\t sensor_dnp_id", "null")
            else:
                for sensor_dnp in sensors_dnp[
                    "content"
                ]:  # informação de sensores modbus paginada
                    sensor_dnp_id = sensor_dnp["id"]
                    print("\t\t sensor_dnp_id", sensor_dnp_id)
                    sensor_dnp_data = await fetch_sensor_dnp_by_id(
                        host=configs.host,
                        auth_token=configs.auth_token,
                        sensor_dnp_id=sensor_dnp_id,
                    )
                    list_sensors_dnp3.append(sensor_dnp_data)
                    sensor_dnp_parsed = parse_sensor_dnp_data(sensor_dnp_data)
                    sensors_dnp_parsed.append(sensor_dnp_parsed)
                    sensors_parsed.append(sensor_parsed)
                    # coletar os registros de cada sensor
                    registers_dnp3 = await collect_registers_dnp(sensor_id)
                    list_registers_dnp3 += registers_dnp3
                    sensor_combine_registers_dnp += combine_primary_with_secondary(
                        sensor_parsed, registers_dnp3
                    )
                    print(
                        "\t\t +sub total resistros por sensor:",
                        len(sensor_combine_registers_dnp),
                    )
                    if DEBUG:
                        break
                    print("total de resgistro por sensor:", len(sensors_dnp_parsed))
            # combinar o resultado de hardware com o resultado de sensores
            hardware_combine_sensors_dnp += combine_primary_with_secondary(
                hardware_parsed, sensor_combine_registers_dnp
            )
            print(
                "\t\t +subtotal de restristros dnp por hardware:",
                len(hardware_combine_sensors_dnp),
            )
            if DEBUG:
                break
        print("total de sensores modbus:", len(hardware_combine_sensors_modbus))
        print("total de sensores dnp3:", len(hardware_combine_sensors_dnp))
        all_flat_data += combine_primary_with_secondary(
            gateway_parsed, hardware_combine_sensors_modbus
        )
        all_flat_data += combine_primary_with_secondary(
            gateway_parsed, hardware_combine_sensors_dnp
        )
        print("total acumulado por hardware:", len(all_flat_data))
    print("total de registros:", len(all_flat_data))
    # Salvar os dados em um arquivo JSON
    with open("data.json", "w") as f:
        json.dump(all_flat_data, f)

    # Criar um DataFrame
    df = pd.DataFrame(all_flat_data)

    # Conectar ao banco SQLite (ou criar um novo se não existir)
    conn = sqlite3.connect("dados.db")

    # Salvar o DataFrame no banco, criando a tabela "dados" (ou sobrescrevendo se já existir)
    df.to_sql("dados", conn, if_exists="replace", index=False)

    # Salvar os acumuladores em arquivos JSON
    with open("cma_gateways.json", "w") as f:
        json.dump(list_gateways, f)
    with open("cma_hardwares.json", "w") as f:
        json.dump(list_hardwares, f)
    # MODBUS
    with open("cma_sensors_modbus.json", "w") as f:
        json.dump(list_sensors_modbus, f)
    with open("registers_modbus.json", "w") as f:
        json.dump(list_registers_modbus, f)
    # DNP3
    with open("cma_sensors_dnp3.json", "w") as f:
        json.dump(list_sensors_dnp3, f)
    with open("cma_registers_dnp3.json", "w") as f:  # noqa
        json.dump(list_registers_dnp3, f)


if __name__ == "__main__":
    asyncio.run(main())
