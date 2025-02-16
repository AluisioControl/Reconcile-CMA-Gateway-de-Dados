import aiohttp


async def fetch_sensors_dnp(
    host: str,
    auth_token: str,
    page: int = 0,
    size: int = 10,
    name: str = None,
    model: str = None,
    gateway_name: str = None,
    type: str = "SENSOR",
    actualization_period: str = "MINUTES",
    active: bool = None,
    manufacturer_id: str = "",
    hardware_id: str = "",
):
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
        "manufacturerId": manufacturer_id,
        "hardwareId": hardware_id,
    }
    if name:
        params["name"] = name
    if model:
        params["model"] = model
    if gateway_name:
        params["gatewayName"] = gateway_name
    if active is not None:
        params["active"] = str(
            active
        ).lower()  # API pode esperar "true" ou "false" como string

    url = f"{host}/sensors-dnp"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(
                f"Falha ao buscar sensores DNP. Código de status: {response.status}"
            )
