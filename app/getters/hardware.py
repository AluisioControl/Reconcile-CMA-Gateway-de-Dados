import aiohttp
import asyncio


async def fetch_hardwares_by_gateway(host: str, auth_token: str, cma_gateway_id: str, name: str = None, active: bool = None):
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
        params["active"] = str(active).lower()  # API pode esperar "true" ou "false" como string

    url = f"{host}/hardwares/all"
    headers = {"Authorization": f"Bearer {auth_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(f"Falha ao buscar hardwares. Código de status: {response.status}")


def parse_hardware_data(data_hardware):
    """
    Converte os campos do hardware para o novo formato especificado.

    Args:
        data_hardware (dict): Dicionário com os dados originais do hardware

    Returns:
        dict: Dicionário com os campos convertidos
    """
    parsed_data = {
        "id_hdw": data_hardware.get("id", None),
        "createdAt_hdw": data_hardware.get("createdAt", None),
        "updatedAt_hdw": data_hardware.get("updatedAt", None),
        "userCreatedId_hdw": data_hardware.get("userCreatedId", None),
        "userUpdatedId_hdw": data_hardware.get("userUpdatedId", None),
        "cmaGatewayId_hdw": data_hardware.get("cmaGatewayId", None),
        "name_hdw": data_hardware.get("name", None),
        "sapId_hdw": data_hardware.get("sapId", None),
        "active_hdw": data_hardware.get("active", None),
        "id_cma": data_hardware.get("cmaGateway", {}).get("id", None),
        "name_cma": data_hardware.get("cmaGateway", {}).get("name", None),
        "ip_cma": data_hardware.get("cmaGateway", {}).get("ip", None),
        "active_cma": data_hardware.get("cmaGateway", {}).get("active", None)
    }
    return parsed_data


curl --location 'https://cma-backend-application.applications.cmapoc.com.br/hardwares/B0D0625C-AFD1-EF11-88F9-6045BDFE79DC' \
--header 'Authorization: ••••••'

async def fetch_gateway_by_id(host, auth_token, gateway_id):
    """
    Obtém detalhes de um gateway específico pelo seu ID.

    Faz uma requisição GET para o endpoint `/cma-gateways/{id}` a fim de recuperar informações detalhadas de um gateway.

    Args:
        gateway_id (str): Identificador único do gateway.

    Returns:
        dict: Dicionário contendo informações detalhadas do gateway.

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.

    Example:
        >>> gateway = await fetch_gateway_by_id("https://api.example.com", "seu_token_aqui", "56B742EF-AED1-EF11-88F9-6045BDFE79DC")
    """
    url = f"{host}/cma-gateways/{gateway_id}"
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                gateway_info = await response.json()
                return gateway_info
            else:
                raise Exception(f"Failed to fetch gateway by ID, status code: {response.status}")