import aiohttp


async def fetch_all_gateways(host, auth_token):
    """
    Obtém a lista de todos os gateways disponíveis.

    Faz uma requisição GET para o endpoint `/cma-gateways/all` a fim de recuperar a lista de gateways cadastrados.

    Args:
        host (str): URL base da API.
        auth_token (str): Token de autenticação Bearer.

    Returns:
        list: Lista de dicionários contendo informações dos gateways.
        exemplo: {'id': '56B742EF-AED1-EF11-88F9-6045BDFE79DC', 'name': 'Gateway 01', 'ip': '100.201.0.5', 'active': True, 'substation': {'id': '09D1D879-7EB2-EF11-88F8-6045BDFE79DC', 'name': 'Taubaté', 'active': True, 'sapAbbreviation': 'TAU'}}

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.

    Example:
        >>> gateways = await fetch_all_gateways("https://api.example.com", "seu_token_aqui")
    """
    url = f"{host}/cma-gateways/all"
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                gateways = await response.json()
                return gateways
            else:
                raise Exception(f"Failed to fetch gateways, status code: {response.status}")


def parse_gateway(data_gateway):
    """
    Converte os campos do gateway para o novo formato especificado.

    Args:
        data_gateway (dict): Dicionário com os dados originais do gateway

    Returns:
        dict: Dicionário com os campos convertidos
    """
    parsed_data = {
        "id_gtw": data_gateway.get("id", None),
        "name_gtw": data_gateway.get("name", None),
        "ip_gtw": data_gateway.get("ip", None),
        "active_gtw": data_gateway.get("active", None),
        "id_sub": data_gateway.get("substation", {}).get("id", None),
        "name_sub": data_gateway.get("substation", {}).get("name", None),
        "active_sub": data_gateway.get("substation", {}).get("active", None),
        "sapAbbreviation_sub": data_gateway.get("substation", {}).get("sapAbbreviation", None),
        "createdAt_gtw": data_gateway.get("createdAt", None),
        "updatedAt_gtw": data_gateway.get("updatedAt", None),
        "userCreatedId_gtw": data_gateway.get("userCreatedId", None),
        "userUpdatedId_gtw": data_gateway.get("userUpdatedId", None),
        "substationId_gtw": data_gateway.get("substationId", None)
    }
    return parsed_data

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

def process_gateway():
    """
    Processa os gateways obtidos e os converte para o novo formato.

    Returns:
        list: Lista de dicionários contendo informações dos gateways convertidos.
    """
    parsed_gateways = []
    gateways = fetch_all_gateways()
    for gateway in gateways:
        data = fetch_gateway_by_id(gateway['id'])
        parsed_gateways.append(parse_gateway(data))
    return parsed_gateways

