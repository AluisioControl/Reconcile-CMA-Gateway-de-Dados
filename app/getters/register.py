import aiohttp


async def fetch_registers_modbus_by_id(
    host: str, auth_token: str, register_modbus_id: str
):
    """
    Obtém um registro Modbus específico pelo seu ID.

    Faz uma requisição GET para o endpoint `/registers-modbus/{id}` a fim de recuperar informações detalhadas de um registro.

    Args:
        host (str): URL base da API.
        auth_token (str): Token de autenticação Bearer.
        register_modbus_id (str): Identificador único do registro Modbus.

    Returns:
        dict: Dicionário contendo informações detalhadas do registro Modbus.

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.

    Example:
        >>> register = await fetch_registers_modbus_by_id("https://api.example.com", "seu_token_aqui", "id_do_registro")
    """

    url = f"{host}/registers-modbus/{register_modbus_id}"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(
                f"Falha ao buscar registro Modbus. Código de status: {response.status}"
            )


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
        params["active"] = str(
            active
        ).lower()  # API pode esperar "true" ou "false" como string

    url = f"{host}/registers-modbus"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(
                f"Falha ao buscar registros Modbus. Código de status: {response.status}"
            )


async def fetch_registers_dnp(
    host: str,
    auth_token: str,
    page: int = 0,
    size: int = 10,
    name: str = "",
    register_data_type: str = "",
    register_control_command: str = "",
    active: bool = None,
    sensor_dnp_id: str = "",
    register_type_id: str = "",
    sensor_type_id: str = "",
):
    """
    Obtém a lista de registros DNP.

    Faz uma requisição GET para o endpoint `/registers-dnp`, com filtros opcionais.

    Args:
        host (str): URL base da API.
        auth_token (str): Token de autenticação Bearer.
        page (int, optional): Número da página. Padrão: 0.
        size (int, optional): Tamanho da página. Padrão: 10.
        name (str, optional): Filtro pelo nome do registro. Padrão: "".
        register_data_type (str, optional): Tipo de dados do registro. Padrão: "".
        register_control_command (str, optional): Comando de controle do registro. Padrão: "".
        active (bool, optional): Filtrar apenas registros ativos (`True`) ou inativos (`False`). Padrão: None.
        sensor_dnp_id (str, optional): ID do sensor DNP. Padrão: "".
        register_type_id (str, optional): ID do tipo de registro. Padrão: "".
        sensor_type_id (str, optional): ID do tipo de sensor. Padrão: "".

    Returns:
        list: Lista de dicionários contendo informações dos registros filtrados.

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.

    Example:
        >>> registers = await fetch_registers_dnp(
        ...     "https://api.example.com",
        ...     "seu_token_aqui",
        ...     page=0,
        ...     size=10,
        ...     name="Registro Y",
        ...     active=True
        ... )
    """

    params = {
        "page": page,
        "size": size,
    }
    if name:
        params["name"] = name
    if register_data_type:
        params["registerDataType"] = register_data_type
    if register_control_command:
        params["registerControlCommand"] = register_control_command
    if sensor_dnp_id:
        params["sensorDnpId"] = sensor_dnp_id
    if register_type_id:
        params["registerTypeId"] = register_type_id
    if sensor_type_id:
        params["sensorTypeId"] = sensor_type_id
    if active is not None:
        params["active"] = str(
            active
        ).lower()  # API pode esperar "true" ou "false" como string

    url = f"{host}/registers-dnp"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(
                f"Falha ao buscar registros DNP. Código de status: {response.status}"
            )


async def fetch_registers_dnp_by_id():
    """
    curl --location 'https://cma-backend-application.applications.cmapoc.com.br/registers-modbus/677535B8-FBC9-EF11-A3F5-5CCD5BDDDDFC' \
--header 'Authorization: ••••••'
    """
    pass
