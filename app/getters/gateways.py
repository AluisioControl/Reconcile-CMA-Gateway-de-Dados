# [GET] {{host}}/cma-gateways/all
# headers: { "Authorization": "Bearer {{auth_token}}" }

# [
#     {
#         "id": "56B742EF-AED1-EF11-88F9-6045BDFE79DC",
#         "name": "Gateway 01",
#         "ip": "100.201.0.5",
#         "active": true,
#         "substation": {
#             "id": "09D1D879-7EB2-EF11-88F8-6045BDFE79DC",
#             "name": "Taubaté",
#             "active": true,
#             "sapAbbreviation": "TAU"
#         }
#     },
#     {
#         "id": "32E7A694-93EB-EF11-88FB-6045BDFE79DC",
#         "name": "Gateway 02",
#         "ip": "152.654.236.987",
#         "active": true,
#         "substation": {
#             "id": "09D1D879-7EB2-EF11-88F8-6045BDFE79DC",
#             "name": "Taubaté",
#             "active": true,
#             "sapAbbreviation": "TAU"
#         }
#     }
# ]

# ---

# [GET] /cma-gateways/:id
# headers: { "Authorization": "Bearer {{auth_token}}" }

# {
#     "id": "56B742EF-AED1-EF11-88F9-6045BDFE79DC",
#     "createdAt": "2025-01-13T13:04:35.030Z",
#     "updatedAt": "2025-02-12T19:30:08.670Z",
#     "userCreatedId": "B2D0D879-7EB2-EF11-88F8-6045BDFE79DC",
#     "userUpdatedId": "3481F89B-D7CD-EF11-88F9-6045BDFE79DC",
#     "substationId": "09D1D879-7EB2-EF11-88F8-6045BDFE79DC",
#     "name": "Gateway 01",
#     "ip": "100.201.0.5",
#     "active": true,
#     "substation": {
#         "id": "09D1D879-7EB2-EF11-88F8-6045BDFE79DC",
#         "name": "Taubaté",
#         "active": true,
#         "sapAbbreviation": "TAU"
#     }
# }

import aiohttp
import asyncio

async def fetch_all_gateways(host, auth_token):
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

async def fetch_gateway_by_id(host, auth_token, gateway_id):
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

async def main():
    import os
    from login import get_auth_token
    host = os.environ.get('GWTDADOS_HOST')
    auth_token = get_auth_token(
        host, 
        username=os.environ.get('GWTDADOS_USERNAME'), 
        password=os.environ.get('GWTDADOS_PASSWORD'))

    try:
        gateways = await fetch_all_gateways(host, auth_token)
        print(f"All Gateways: {gateways}")

        # Exemplo para coletar informações de um gateway específico
        gateway_id = "56B742EF-AED1-EF11-88F9-6045BDFE79DC"  # Substitua pelo ID do gateway
        gateway_info = await fetch_gateway_by_id(host, auth_token, gateway_id)
        print(f"Gateway Info [{gateway_id}]: {gateway_info}")

    except Exception as e:
        print(f"Error: {e}")

# Executa o loop de eventos
if __name__ == "__main__":
    asyncio.run(main())