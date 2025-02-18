import aiohttp


async def fetch_register_modbus_by_id(
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

    # Tenta até 3 vezes se der timeout
    for attempt in range(1, 4):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    raise Exception(
                        f"Falha ao buscar registro Modbus. Código de status: {response.status}"
                    )
        except aiohttp.client_exceptions.ConnectionTimeoutError:
            print(f"Tentativa {attempt}: deu timeout, bora tentar de novo...")
            if attempt == 3:
                raise Exception("Timeout persistente após 3 tentativas")


async def fetch_registers_modbus(
    host: str,
    auth_token: str,
    page: int = None,
    size: int = None,
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

    params = {}
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
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
    page: int = None,
    size: int = None,
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

    params = {}
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
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


async def fetch_register_dnp_by_id(host: str, auth_token: str, register_dnp_id: str):
    """
    Obtém um registro DNP específico pelo seu ID.

    Faz uma requisição GET para o endpoint `/registers-dnp/{id}` a fim de recuperar informações detalhadas de um registro.

    Args:
        host (str): URL base da API.
        auth_token (str): Token de autenticação Bearer.
        register_dnp_id (str): Identificador único do registro DNP.

    Returns:
        dict: Dicionário contendo informações detalhadas do registro DNP.

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.

    Example:
        >>> register = await fetch_registers_dnp_by_id("https://api.example.com", "seu_token_aqui", "id_do_registro")
    """

    url = f"{host}/registers-dnp/{register_dnp_id}"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(
                f"Falha ao buscar registro DNP. Código de status: {response.status}"
            )


def parse_register_modbus_data(data_register_modbus):
    """
    Converte os campos do registro Modbus para o novo formato especificado.

    Args:
        data_register_modbus (dict): Dicionário com os dados originais do registro Modbus

    Returns:
        dict: Dicionário com os campos convertidos
    """
    parsed_data = {
        "id_reg_mod": data_register_modbus.get("id", None),
        "createdAt_reg_mod": data_register_modbus.get("createdAt", None),
        "updatedAt_reg_mod": data_register_modbus.get("updatedAt", None),
        "userCreatedId_reg_mod": data_register_modbus.get("userCreatedId", None),
        "userUpdatedId_reg_mod": data_register_modbus.get("userUpdatedId", None),
        "sensorModbusId_reg_mod": data_register_modbus.get("sensorModbusId", None),
        "registerTypeId_reg_mod": data_register_modbus.get("registerTypeId", None),
        "sensorTypeId_reg_mod": data_register_modbus.get("sensorTypeId", None),
        "name_reg_mod": data_register_modbus.get("name", None),
        "description_reg_mod": data_register_modbus.get("description", None),
        "addressSlave_reg_mod": data_register_modbus.get("addressSlave", None),
        "addressRegister_reg_mod": data_register_modbus.get("addressRegister", None),
        "registerModbusType_reg_mod": data_register_modbus.get(
            "registerModbusType", None
        ),
        "registerDataFormat_reg_mod": data_register_modbus.get(
            "registerDataFormat", None
        ),
        "bit_reg_mod": data_register_modbus.get("bit", None),
        "multiplier_reg_mod": data_register_modbus.get("multiplier", None),
        "additive_reg_mod": data_register_modbus.get("additive", None),
        "active_reg_mod": data_register_modbus.get("active", None),
        "id_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get("id", None),
        "name_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get(
            "name", None
        ),
        "description_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get(
            "description", None
        ),
        "model_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get(
            "model", None
        ),
        "ip_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get("ip", None),
        "port_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get(
            "port", None
        ),
        "type_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get(
            "type", None
        ),
        "attempts_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get(
            "attempts", None
        ),
        "timeLimit_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get(
            "timeLimit", None
        ),
        "actualizationPeriod_sen_reg_mod": data_register_modbus.get(
            "sensorModbus", {}
        ).get("actualizationPeriod", None),
        "actualizationTime_sen_reg_mod": data_register_modbus.get(
            "sensorModbus", {}
        ).get("actualizationTime", None),
        "maxRegisterRead_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get(
            "maxRegisterRead", None
        ),
        "maxRegisterWrite_sen_reg_mod": data_register_modbus.get(
            "sensorModbus", {}
        ).get("maxRegisterWrite", None),
        "maxRegisterBitsRead_sen_reg_mod": data_register_modbus.get(
            "sensorModbus", {}
        ).get("maxRegisterBitsRead", None),
        "active_sen_reg_mod": data_register_modbus.get("sensorModbus", {}).get(
            "active", None
        ),
        "id_man_reg_mod": data_register_modbus.get("sensorModbus", {})
        .get("manufacturer", {})
        .get("id", None),
        "name_man_reg_mod": data_register_modbus.get("sensorModbus", {})
        .get("manufacturer", {})
        .get("name", None),
        "active_man_reg_mod": data_register_modbus.get("sensorModbus", {})
        .get("manufacturer", {})
        .get("active", None),
        "id_reg_reg_mod": data_register_modbus.get("registerType", {}).get("id", None),
        "name_reg_reg_mod": data_register_modbus.get("registerType", {}).get(
            "name", None
        ),
        "active_reg_reg_mod": data_register_modbus.get("registerType", {}).get(
            "active", None
        ),
        "id_sen_reg_mod": data_register_modbus.get("sensorType", {}).get("id", None),
        "name_sen_reg_mod": data_register_modbus.get("sensorType", {}).get(
            "name", None
        ),
        "active_sen_reg_mod": data_register_modbus.get("sensorType", {}).get(
            "active", None
        ),
    }
    return parsed_data


def parse_register_dnp_data(data_reg_dnp3):
    """
    Converte os campos do registro DNP para o novo formato especificado.

    Args:
        data_reg_dnp3 (dict): Dicionário com os dados originais do registro DNP

    Returns:
        dict: Dicionário com os campos convertidos
    """
    parsed_data = {
        "id_reg_dnp3": data_reg_dnp3.get("id", None),
        "createdAt_reg_dnp3": data_reg_dnp3.get("createdAt", None),
        "updatedAt_reg_dnp3": data_reg_dnp3.get("updatedAt", None),
        "userCreatedId_reg_dnp3": data_reg_dnp3.get("userCreatedId", None),
        "userUpdatedId_reg_dnp3": data_reg_dnp3.get("userUpdatedId", None),
        "sensorDnpId_reg_dnp3": data_reg_dnp3.get("sensorDnpId", None),
        "registerTypeId_reg_dnp3": data_reg_dnp3.get("registerTypeId", None),
        "sensorTypeId_reg_dnp3": data_reg_dnp3.get("sensorTypeId", None),
        "name_reg_dnp3": data_reg_dnp3.get("name", None),
        "description_reg_dnp3": data_reg_dnp3.get("description", None),
        "index_reg_dnp3": data_reg_dnp3.get("index", None),
        "timeOn_reg_dnp3": data_reg_dnp3.get("timeOn", None),
        "timeOff_reg_dnp3": data_reg_dnp3.get("timeOff", None),
        "registerDataType_reg_dnp3": data_reg_dnp3.get("registerDataType", None),
        "registerControlCommand_reg_dnp3": data_reg_dnp3.get(
            "registerControlCommand", None
        ),
        "active_reg_dnp3": data_reg_dnp3.get("active", None),
        "id_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get("id", None),
        "name_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get("name", None),
        "description_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get(
            "description", None
        ),
        "model_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get("model", None),
        "ip_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get("ip", None),
        "port_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get("port", None),
        "type_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get("type", None),
        "attempts_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get(
            "attempts", None
        ),
        "timeLimit_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get(
            "timeLimit", None
        ),
        "actualizationPeriod_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get(
            "actualizationPeriod", None
        ),
        "pollRbePeriod_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get(
            "pollRbePeriod", None
        ),
        "pollStaticPeriod_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get(
            "pollStaticPeriod", None
        ),
        "addressSource_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get(
            "addressSource", None
        ),
        "addressSlave_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get(
            "addressSlave", None
        ),
        "active_dnp_reg_dnp3": data_reg_dnp3.get("sensorDnp", {}).get("active", None),
        "id_man_reg_dnp3": data_reg_dnp3.get("manufacturer", {}).get("id", None),
        "name_man_reg_dnp3": data_reg_dnp3.get("manufacturer", {}).get("name", None),
        "active_man_reg_mod": data_reg_dnp3.get("manufacturer", {}).get("active", None),
        "id_reg_reg_dnp3": data_reg_dnp3.get("registerType", {}).get("id", None),
        "name_reg_reg_dnp3": data_reg_dnp3.get("registerType", {}).get("name", None),
        "active_reg_reg_dnp_dnp3": data_reg_dnp3.get("registerType", {}).get(
            "active", None
        ),
        "id_sen_reg_dnp3": data_reg_dnp3.get("sensorType", {}).get("id", None),
        "name_sen_reg_dnp3": data_reg_dnp3.get("sensorType", {}).get("name", None),
        "active_sen_reg_dnp3": data_reg_dnp3.get("sensorType", {}).get("active", None),
    }
    return parsed_data
