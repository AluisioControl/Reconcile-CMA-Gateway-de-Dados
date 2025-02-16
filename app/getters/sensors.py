
import aiohttp

async def fetch_sensors_modbus(host: str, auth_token: str, page: int = 0, size: int = 10, name: str = None, model: str = None, gateway_name: str = None, type: str = "SENSOR", actualization_period: str = "MINUTES", active: bool = None, manufacturer_id: str = None, hardware_id: str = None):
    """
    Obtém a lista de sensores Modbus.

    Faz uma requisição GET para o endpoint `/sensors-modbus`, filtrando os resultados pelos parâmetros fornecidos.

    Args:
        host (str): URL base da API.
        auth_token (str): Token de autenticação Bearer.
        page (int, optional): Número da página. Padrão: 0.
        size (int, optional): Tamanho da página. Padrão: 10.
        name (str, optional): Filtro pelo nome do sensor. Padrão: None.
        model (str, optional): Filtro pelo modelo do sensor. Padrão: None.
        gateway_name (str, optional): Filtro pelo nome do gateway. Padrão: None.
        type (str, optional): Tipo do sensor. Padrão: "SENSOR".
        actualization_period (str, optional): Período de atualização. Padrão: "MINUTES".
        active (bool, optional): Filtrar apenas sensores ativos (`True`) ou inativos (`False`). Padrão: None.
        manufacturer_id (str, optional): Filtro pelo ID do fabricante. Padrão: None.
        hardware_id (str, optional): Filtro pelo ID do hardware. Padrão: None.

    Returns:
        list: Lista de dicionários contendo informações dos sensores filtrados.

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.
    """
    params = {
        "page": page,
        "size": size,
        "type": type,
        "actualizationPeriod": actualization_period
    }
    if name:
        params["name"] = name
    if model:
        params["model"] = model
    if gateway_name:
        params["gatewayName"] = gateway_name
    if active is not None:
        params["active"] = str(active).lower()  # API pode esperar "true" ou "false" como string
    if manufacturer_id:
        params["manufacturerId"] = manufacturer_id
    if hardware_id:
        params["hardwareId"] = hardware_id

    url = f"{host}/sensors-modbus"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(f"Falha ao buscar sensores Modbus. Código de status: {response.status}")


async def fetch_sensors_dnp(host: str, auth_token: str, page: int = 0, size: int = 10, name: str = None, model: str = None, gateway_name: str = None, type: str = "SENSOR", actualization_period: str = "MINUTES", active: bool = None, manufacturer_id: str = "", hardware_id: str = ""):
    """
    Obtém a lista de sensores DNP.

    Faz uma requisição GET para o endpoint `/sensors-dnp`, filtrando os resultados pelos parâmetros fornecidos.

    Args:
        host (str): URL base da API.
        auth_token (str): Token de autenticação Bearer.
        page (int, optional): Número da página. Padrão: 0.
        size (int, optional): Tamanho da página. Padrão: 10.
        name (str, optional): Filtro pelo nome do sensor. Padrão: None.
        model (str, optional): Filtro pelo modelo do sensor. Padrão: None.
        gateway_name (str, optional): Filtro pelo nome do gateway. Padrão: None.
        type (str, optional): Tipo de sensor. Padrão: "SENSOR".
        actualization_period (str, optional): Período de atualização. Padrão: "MINUTES".
        active (bool, optional): Filtrar apenas sensores ativos (`True`) ou inativos (`False`). Padrão: None.
        manufacturer_id (str, optional): Filtro pelo ID do fabricante. Padrão: "".
        hardware_id (str, optional): Filtro pelo ID do hardware. Padrão: "".

    Returns:
        list: Lista de dicionários contendo informações dos sensores filtrados.

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.
    """
    params = {
        "page": page,
        "size": size,
        "type": type,
        "actualizationPeriod": actualization_period,
        "hardwareId": hardware_id
    }
    if name:
        params["name"] = name
    if manufacturer_id:
        params["manufacturerId"] = manufacturer_id
    if model:
        params["model"] = model
    if gateway_name:
        params["gatewayName"] = gateway_name
    if active is not None:
        params["active"] = str(active).lower()  # API pode esperar "true" ou "false" como string

    url = f"{host}/sensors-dnp"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(f"Falha ao buscar sensores DNP. Código de status: {response.status}")

def parse_sensor_modbus_data(data_sensores):
    """
    Converte os campos do sensor para o novo formato especificado.

    Args:
        data_sensores (dict): Dicionário com os dados originais do sensor

    Returns:
        dict: Dicionário com os campos convertidos
    """
    parsed_data = {
        "id_sen": data_sensores.get("id", None),
        "createdAt_sen": data_sensores.get("createdAt", None),
        "updatedAt_sen": data_sensores.get("updatedAt", None),
        "userCreatedId_sen": data_sensores.get("userCreatedId", None),
        "userUpdatedId_sen": data_sensores.get("userUpdatedId", None),
        "manufacturerId_sen": data_sensores.get("manufacturerId", None),
        "hardwareId_sen": data_sensores.get("hardwareId", None),
        "name_sen": data_sensores.get("name", None),
        "description_sen": data_sensores.get("description", None),
        "model_sen": data_sensores.get("model", None),
        "ip_sen": data_sensores.get("ip", None),
        "port_sen": data_sensores.get("port", None),
        "type_sen": data_sensores.get("type", None),
        "attempts_sen": data_sensores.get("attempts", None),
        "timeLimit_sen": data_sensores.get("timeLimit", None),
        "actualizationPeriod_sen": data_sensores.get("actualizationPeriod", None),
        "actualizationTime_sen": data_sensores.get("actualizationTime", None),
        "maxRegisterRead_sen": data_sensores.get("maxRegisterRead", None),
        "maxRegisterWrite_sen": data_sensores.get("maxRegisterWrite", None),
        "maxRegisterBitsRead_sen": data_sensores.get("maxRegisterBitsRead", None),
        "active_sen": data_sensores.get("active", None),
        "id_man": data_sensores.get("manufacturer", {}).get("id", None),
        "name_man": data_sensores.get("manufacturer", {}).get("name", None),
        "active_man": data_sensores.get("manufacturer", {}).get("active", None),
        "id_hw_sen": data_sensores.get("hardware", {}).get("id", None),
        "name_hw_sen": data_sensores.get("hardware", {}).get("name", None),
        "sapId_hd_sen": data_sensores.get("hardware", {}).get("sapId", None)
    }
    return parsed_data

def parse_sensor_dnp3_data(data_sensor_dnp3):
    """
    Converte os campos do sensor DNP3 para o novo formato especificado.

    Args:
        data_sensor_dnp3 (dict): Dicionário com os dados originais do sensor DNP3

    Returns:
        dict: Dicionário com os campos convertidos
    """
    parsed_data = {
        "id_sen_dnp3": data_sensor_dnp3.get("id", None),
        "createdAt_sen_dnp3": data_sensor_dnp3.get("createdAt", None),
        "updatedAt_sen_dnp3": data_sensor_dnp3.get("updatedAt", None),
        "userCreatedId_sen_dnp3": data_sensor_dnp3.get("userCreatedId", None),
        "userUpdatedId_sen_dnp3": data_sensor_dnp3.get("userUpdatedId", None),
        "manufacturerId_sen_dnp3": data_sensor_dnp3.get("manufacturerId", None),
        "hardwareId_sen_dnp3": data_sensor_dnp3.get("hardwareId", None),
        "name_sen_dnp3": data_sensor_dnp3.get("name", None),
        "description_sen_dnp3": data_sensor_dnp3.get("description", None),
        "model_sen_dnp3": data_sensor_dnp3.get("model", None),
        "ip_sen_dnp3": data_sensor_dnp3.get("ip", None),
        "port_sen_dnp3": data_sensor_dnp3.get("port", None),
        "type_sen_dnp3": data_sensor_dnp3.get("type", None),
        "attempts_sen_dnp3": data_sensor_dnp3.get("attempts", None),
        "timeLimit_sen_dnp3": data_sensor_dnp3.get("timeLimit", None),
        "actualizationPeriod_sen_dnp3": data_sensor_dnp3.get("actualizationPeriod", None),
        "pollRbePeriod_sen_dnp3": data_sensor_dnp3.get("pollRbePeriod", None),
        "pollStaticPeriod_sen_dnp3": data_sensor_dnp3.get("pollStaticPeriod", None),
        "addressSource_sen_dnp3": data_sensor_dnp3.get("addressSource", None),
        "addressSlave_sen_dnp3": data_sensor_dnp3.get("addressSlave", None),
        "active_sen_dnp3": data_sensor_dnp3.get("active", None),
        
        # Manufacturer data
        "id_sen_dnp3_man": data_sensor_dnp3.get("manufacturer", {}).get("id", None),
        "name_sen_dnp3_man": data_sensor_dnp3.get("manufacturer", {}).get("name", None),
        "active_sen_dnp3_man": data_sensor_dnp3.get("manufacturer", {}).get("active", None),
        
        # Hardware data
        "id_sen_dnp3_hw": data_sensor_dnp3.get("hardware", {}).get("id", None),
        "name_sen_dnp3_hw": data_sensor_dnp3.get("hardware", {}).get("name", None),
        "sapId_sen_dnp3_hw": data_sensor_dnp3.get("hardware", {}).get("sapId", None),
        "active_sen_dnp3_hw": data_sensor_dnp3.get("hardware", {}).get("active", None),
        
        # CMA data
        "id_sen_dnp3_cma": data_sensor_dnp3.get("cma", {}).get("id", None),
        "name_sen_dnp3_cma": data_sensor_dnp3.get("cma", {}).get("name", None),
        "ip_sen_dnp3_cma": data_sensor_dnp3.get("cma", {}).get("ip", None),
        "active_sen_dnp3_cma": data_sensor_dnp3.get("cma", {}).get("active", None)
    }
    return parsed_data
