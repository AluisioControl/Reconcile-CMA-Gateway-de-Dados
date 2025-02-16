import aiohttp
import asyncio
import json
import os


async def get_auth_token(host: str, username: str, password: str):
    url = f"{host}/auth/token"
    headers = {"Content-Type": "application/json"}
    payload = {"username": username, "password": password}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 201:
                token_response = await response.json()
                return token_response.get(
                    "access_token"
                )  # Assumindo que o token está nesta chave
            else:
                # Gerencia o erro de autenticação
                raise Exception(f"Failed to get token, status code: {response.status}")
        response


if __name__ == "__main__":
    host = os.environ.get("GWTDADOS_HOST")
    username = os.environ.get("GWTDADOS_USERNAME")
    password = os.environ.get("GWTDADOS_PASSWORD")

    try:
        token = asyncio.run(get_auth_token(host, username, password))
        print(f"Received token: {token}")
    except Exception as e:
        print(f"Error: {e}")
