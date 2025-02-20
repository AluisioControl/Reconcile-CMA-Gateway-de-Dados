import asyncio
import aiohttp
from app.utils.http_utils import fetch_with_retry


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
    return await fetch_with_retry(url=url, headers=headers, params=params)


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
        "active_cma": data_hardware.get("cmaGateway", {}).get("active", None),
    }
    return parsed_data


async def fetch_hardware_by_id(host, auth_token, hardware_id):
    """
    Obtém detalhes de um hardware específico pelo seu ID.

    Faz uma requisição GET para o endpoint `/hardwares/{id}` a fim de recuperar informações detalhadas de um hardware.

    Args:
        host (str): URL base da API.
        auth_token (str): Token de autenticação Bearer.
        hardware_id (str): Identificador único do hardware.

    Returns:
        dict: Dicionário contendo informações detalhadas do hardware.

    Raises:
        Exception: Se a requisição falhar ou retornar um status diferente de 200.

    Example:
        >>> hardware = await fetch_hardware_by_id("https://api.example.com", "seu_token_aqui", "B0D0625C-AFD1-EF11-88F9-6045BDFE79DC")
    """
    url = f"{host}/hardwares/{hardware_id}"
    headers = {"Authorization": f"Bearer {auth_token}"}
    return await fetch_with_retry(url=url, headers=headers)


if __name__ == "__main__":
    import asyncio
    import os
    from app.settings import configs
    from tests.conftest import gateways

    async def main():
        cma_gateway_id = gateways[1]["id"]
        hardwares = await fetch_hardwares_by_gateway(configs.host, configs.auth_token, cma_gateway_id=cma_gateway_id)
        print("All hardwares:")
        print(hardwares)

    asyncio.run(main())
