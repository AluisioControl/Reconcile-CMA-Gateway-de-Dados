import asyncio
import json
import os
import sys
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
from app.logger import logger
from app.utils.data import combine_primary_with_secondary

from .settings import configs

semaphore = Semaphore(configs.MAX_PARALLEL_REQUESTS)


async def fetch_and_parse_register_modbus(register_data):
    async with semaphore:
        register_data = await fetch_register_modbus_by_id(
            host=configs.host,
            auth_token=await configs.auth_token,
            register_modbus_id=register_data["id"],
        )
        return parse_register_modbus_data(register_data)


async def collect_registers_modbus(sensor_modbus_id):
    registers = []
    registers_data = await fetch_registers_modbus(
        host=configs.host,
        auth_token=await configs.auth_token,
        sensor_modbus_id=sensor_modbus_id,
        size=configs.MAX_PAGE_SIZE,
    )
    print(
        f"   - Coletando {len(registers_data["content"])} registros modbus sensor id: {sensor_modbus_id}..."
    )
    # processar os registros em paralelo
    tasks = [
        fetch_and_parse_register_modbus(register_data)
        for register_data in registers_data["content"]
    ]
    logger.info(f"   - Coletando {len(tasks)} registros")
    registers = await asyncio.gather(*tasks)
    return registers


async def fetch_and_parse_register_dnp(register_data):
    async with semaphore:
        register_data = await fetch_register_dnp_by_id(
            host=configs.host,
            auth_token=await configs.auth_token,
            register_dnp_id=register_data["id"],
        )
    return parse_register_dnp_data(register_data)


async def collect_registers_dnp(sensor_dnp_id):
    registers = []
    registers_data = await fetch_registers_dnp(
        host=configs.host,
        auth_token=await configs.auth_token,
        sensor_dnp_id=sensor_dnp_id,
        size=configs.MAX_PAGE_SIZE,
    )
    print(
        f"   - Coletando {len(registers_data["content"])} registros dnp3 sensor id: {sensor_dnp_id}..."
    )
    # processar os registros em paralelo
    tasks = [
        fetch_and_parse_register_dnp(register_data)
        for register_data in registers_data["content"]
    ]
    logger.info("    - Coletando ", len(tasks), " registros")
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
        host=configs.host, auth_token=await configs.auth_token
    )
    logger.info(f"gateway disponíveis: {", ".join([gw["name"] for gw in gateways])}")
    if not gateways:
        print(f"\033[91m >>> Nenhum gateway disponível <<< \x1b[0m")
    # get gateway by name
    gateways_founds = [
        gateway for gateway in gateways if gateway["name"] == configs.gateway_name
    ]
    if not gateways_founds:
        logger.error(f"Gateway {configs.gateway_name} não encontrado")
        print(f"\033[91m >>> Gateway {configs.gateway_name} não encontrado <<< \x1b[0m")
        print(f"\033[93m >>> Gateways disponíveis: {', '.join([gw['name'] for gw in gateways])} <<< \x1b[0m")
        raise ValueError(f"Gateway {configs.gateway_name} não encontrado")
    for gateway in gateways_founds:
        gateway_id = gateway["id"]
        print(f"gateway name: {gateway["name"]}")
        logger.info(f"gateway name: {gateway["name"]}")
        gateway_data = await fetch_gateway_by_id(
            host=configs.host,
            auth_token=await configs.auth_token,
            gateway_id=gateway_id,
        )
        list_gateways.append(gateway_data)
        gateway_parsed = parse_gateway_data(gateway_data)
        hardware_combine_sensors_modbus = []
        hardware_combine_sensors_dnp = []
        hardwares = await fetch_hardwares_by_gateway(
            host=configs.host,
            auth_token=await configs.auth_token,
            cma_gateway_id=gateway_id,
        )
        for hardware in hardwares:
            hardware_id = hardware["id"]
            logger.info(f"  nome hardware {hardware["name"]}")
            hardware_data = await fetch_hardware_by_id(
                host=configs.host,
                auth_token=await configs.auth_token,
                hardware_id=hardware_id,
            )
            list_hardwares.append(hardware_data)
            hardware_parsed = parse_hardware_data(hardware_data)
            # hardwares_parsed.append(hardware_parsed)

            # consultar todos os sensor MODBUS associado a cada hardware
            sensors_parsed = []
            sensors = await fetch_sensors_modbus(
                host=configs.host,
                auth_token=await configs.auth_token,
                hardware_id=hardware_id,
            )
            sensor_combine_registers_modbus = []
            if not sensors["content"]:
                logger.warning(f"O hardware id: {hardware_id} não tem modbus dnp3")
            else:
                print(f"Coleando sensores {len(sensors)} modbus...")
                for sensor in sensors[
                    "content"
                ]:  # informação de sensores modbus paginada
                    sensor_id = sensor["id"]
                    logger.info(f"   Nome sensor modbus: {sensor["name"]}")
                    sensor_data = await fetch_sensor_modbus_by_id(
                        host=configs.host,
                        auth_token=await configs.auth_token,
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
                    logger.info(
                        f"   +sub total resistros por sensor: {len(sensor_combine_registers_modbus)}",
                    )
                    if configs.DEBUG:
                        break
            # combinar o resultado de hardware com o resultado de sensores
            hardware_combine_sensors_modbus += combine_primary_with_secondary(
                hardware_parsed, sensor_combine_registers_modbus
            )
            logger.info(
                f"  +subtotal de restristros por hardware: {len(hardware_combine_sensors_modbus)}"
            )
            # hardwares_combined += hardware_combine_sensors_modbus

            # consultar todos os sensor DNP associado a cada hardware
            sensors_dnp_parsed = []
            sensors_dnp = await fetch_sensors_dnp(
                host=configs.host,
                auth_token=await configs.auth_token,
                active=True,
                hardware_id=hardware_id,
            )
            sensor_combine_registers_dnp = []
            if not sensors_dnp["content"]:
                logger.warning(f"O hardware id: {hardware_id} não tem sensores dnp3")
            else:
                print(f"Coleando sensores {len(sensors_dnp)} dnp3...")
                for sensor_dnp in sensors_dnp[
                    "content"
                ]:  # informação de sensores modbus paginada
                    sensor_dnp_id = sensor_dnp["id"]
                    logger.info("  sensor_dnp_id", sensor_dnp_id)
                    sensor_dnp_data = await fetch_sensor_dnp_by_id(
                        host=configs.host,
                        auth_token=await configs.auth_token,
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
                    logger.info(
                        "  +sub total resistros por sensor:",
                        len(sensor_combine_registers_dnp),
                    )
                    if configs.DEBUG:
                        break
                    logger.info(
                        "total de resgistro por sensor:", len(sensors_dnp_parsed)
                    )
            # combinar o resultado de hardware com o resultado de sensores
            hardware_combine_sensors_dnp += combine_primary_with_secondary(
                hardware_parsed, sensor_combine_registers_dnp
            )
            logger.info(
                f"  +subtotal de restristros dnp por hardware: {len(hardware_combine_sensors_dnp)}"
            )
            if configs.DEBUG:
                break
        logger.info(f"total de sensores modbus: {len(hardware_combine_sensors_modbus)}")
        logger.info(f"total de sensores dnp3: {len(hardware_combine_sensors_dnp)}")
        all_flat_data += combine_primary_with_secondary(
            gateway_parsed, hardware_combine_sensors_modbus
        )
        all_flat_data += combine_primary_with_secondary(
            gateway_parsed, hardware_combine_sensors_dnp
        )
        logger.info(f"total acumulado por hardware: {len(all_flat_data)}")
    logger.info(f"total de registros: {len(all_flat_data)}")
    # Salvar os dados em um arquivo JSON
    with open("data.json", "w") as f:
        json.dump(all_flat_data, f)

    # verificar se o all_flat_data está vazio
    if not all_flat_data:
        logger.warning("Nenhum dado coletado")
        return

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
