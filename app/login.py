import aiohttp
import asyncio
import json
import os

async def get_auth_token(host:str, username: str, password: str):
    url = f"{host}/auth/token"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "username": username,
        "password": password
    }

    async with aiohttp.ClientSession() as session:
        print(f"Requesting token from {url}")
        async with session.post(url, headers=headers, json=payload) as response:
            print(f"Response status: {response.status}")
            if response.status == 201:
                token_response = await response.json()
                return token_response.get('access_token')  # Assumindo que o token está nesta chave
            else:
                # Gerencia o erro de autenticação
                raise Exception(f"Failed to get token, status code: {response.status}")
        response

