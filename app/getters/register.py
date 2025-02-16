import aiohttp

import aiohttp


async def fetch_registers_modbus(
    host: str,
    auth_token: str,
    page: int = 0,
    size: int = 10,
    name: str = "",
    register_modbus_type: str = "",
    register_data_format: str = "",
    active: bool = None,
    sensor_modbus_id: str = "",
    register_type_id: str = "",
    sensor_type_id: str = "",
):
    """
    Obtém a lista de registros Modbus.

    Faz uma requisição GET para o endpoint `/registers-modbus`, com filtros opcionais.

    Args:
        host (str): URL base da API.
        auth_token (str): Token de autenticação Bearer.
        page (int, optional): Número da página. Padrão: 0.
        size (int, optional): Tamanho da página. Padrão: 10.
        name (str, optional): Filtro pelo nome do registro. Padrão: "".
        register_modbus_type (str, optional): Tipo de registro Modbus. Padrão: "".
        register_data_format (str, optional): Formato de dados do registro. Padrão: "".
        active (bool, optional): Filtrar apenas registros ativos (`True`) ou inativos (`False`). Padrão: None.
        sensor_modbus_id (str, optional): ID do sensor Modbus. Padrão: "".
        register_type_id (str, optional): ID do tipo de registro. Padrão: "".
        sensor_type_id (str, optional): ID do tipo de sensor. Padrão: "".

    Returns:
        list: Lista de dicionários contendo informações dos registros filtrados.

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.

    Example:
        >>> registers = await fetch_registers_modbus(
        ...     "https://api.example.com",
        ...     "seu_token_aqui",
        ...     page=0,
        ...     size=10,
        ...     name="Registro X",
        ...     active=True
        ... )
    """

    params = {
        "page": page,
        "size": size,
    }
    if name:
        params["name"] = name
    if register_modbus_type:
        params["registerModbusType"] = register_modbus_type
    if register_data_format:
        params["registerDataFormat"] = register_data_format
    if sensor_modbus_id:
        params["sensorModbusId"] = sensor_modbus_id
    if register_type_id:
        params["registerTypeId"] = register_type_id
    if sensor_type_id:
        params["sensorTypeId"] = sensor_type_id
    if active is not None:
        params["active"] = str(active).lower()  # API pode esperar "true" ou "false" como string

    url = f"{host}/registers-modbus"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(
                f"Falha ao buscar registros Modbus. Código de status: {response.status}"
            )


async def fetch_registers_dnp():
    """
    curl --location 'https://cma-backend-application.applications.cmapoc.com.br/sensors-dnp?page=0&size=10&name=sens&model=model&gatewayName=Gateway%201&type=SENSOR&actualizationPeriod=MINUTES&active=true&manufacturerId=&hardwareId=' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNDgxRjg5Qi1EN0NELUVGMTEtODhGOS02MDQ1QkRGRTc5REMiLCJ1c2VybmFtZSI6ImNvbnRyb2xAYXRsYW50aWNvLmNvbSIsImNsYWltcyI6WzIwMCwzMDAsNDAwXSwiaWF0IjoxNzM5NzA4MjczLCJleHAiOjE3Mzk3MTU0NzN9.rpkdDJX8ej9Zi_kLAQ7nyttdoqQcei4SvxHqPB2cGuQ'
    """
    raise NotImplementedError("This function is not yet implemented")
