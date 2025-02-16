import aiohttp


async def fetch_hardwares_by_gateway(
    host: str,
    auth_token: str,
    cma_gateway_id: str,
    name: str = None,
    active: bool = None,
):
    """
    Obtém a lista de hardwares associados a um gateway específico.

    Faz uma requisição GET para o endpoint `/hardwares/all`, filtrando os resultados pelo `cmaGatewayId`.
    Filtros opcionais como `name` e `active` podem ser utilizados para refinar a busca.

    Args:
        host (str): URL base da API.
        auth_token (str): Token de autenticação Bearer.
        cma_gateway_id (str): Identificador único do gateway associado aos hardwares.
        name (str, optional): Filtro pelo nome do hardware. Padrão: None.
        active (bool, optional): Filtrar apenas hardwares ativos (`True`) ou inativos (`False`). Padrão: None.

    Returns:
        list: Lista de dicionários contendo informações dos hardwares filtrados.

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.

    Example:
        >>> hardwares = await fetch_hardwares_by_gateway(
        ...     "https://api.example.com",
        ...     "seu_token_aqui",
        ...     "8465F883-FAC9-EF11-A3F5-5CCD5BDDDDFC",
        ...     name="Sensor X",
        ...     active=True
        ... )
    """
    params = {"cmaGatewayId": cma_gateway_id}
    if name:
        params["name"] = name
    if active is not None:
        params["active"] = str(
            active
        ).lower()  # API pode esperar "true" ou "false" como string

    url = f"{host}/hardwares/all"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(
                f"Falha ao buscar hardwares. Código de status: {response.status}"
            )


async def fetch_registers_modbus():
    """
    curl --location 'https://cma-backend-application.applications.cmapoc.com.br/registers-modbus?page=0&size=10&name=&registerModbusType=&registerDataFormat=&active=&sensorModbusId=&registerTypeId=&sensorTypeId=' --header 'Authorization: ••••••'
    """
    raise NotImplementedError("This function is not yet implemented")


async def fetch_registers_dnp():
    """
    curl --location 'https://cma-backend-application.applications.cmapoc.com.br/sensors-dnp?page=0&size=10&name=sens&model=model&gatewayName=Gateway%201&type=SENSOR&actualizationPeriod=MINUTES&active=true&manufacturerId=&hardwareId=' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNDgxRjg5Qi1EN0NELUVGMTEtODhGOS02MDQ1QkRGRTc5REMiLCJ1c2VybmFtZSI6ImNvbnRyb2xAYXRsYW50aWNvLmNvbSIsImNsYWltcyI6WzIwMCwzMDAsNDAwXSwiaWF0IjoxNzM5NzA4MjczLCJleHAiOjE3Mzk3MTU0NzN9.rpkdDJX8ej9Zi_kLAQ7nyttdoqQcei4SvxHqPB2cGuQ'
    """
    raise NotImplementedError("This function is not yet implemented")
