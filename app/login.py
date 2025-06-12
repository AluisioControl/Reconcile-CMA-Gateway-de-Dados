import asyncio
import os
import sys
import aiohttp

from app.logger import logger


async def get_auth_token(host: str, username: str, password: str):
    url = f"{host}/auth/token"
    headers = {"Content-Type": "application/json"}
    payload = {"username": username, "password": password}

    try: 
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 201:
                    token_response = await response.json()
                    return token_response.get("access_token")  # Assumindo que o token está nesta chave
                else:
                    # Gerencia o erro de autenticação
                    msg = f"Failed to get token, status code: {response.status}"
                    logger.error(msg)
                    print(msg)
                    if response.status == 401:
                        print("Credenciais inválidas. Por favor, verifique seu nome de usuário e senha.")
                    elif response.status == 403:
                        print("Acesso negado. Você não tem permissão para acessar este recurso.")
                    else:
                        print(f"Erro desconhecido: {response.status}")
                    print("Tente novamente ou entre em contato com o administrador do sistema.")
                    sys.exit(1)
            response
    except ConnectionError as e:
        msg = f"Ocorreu um erro ao tentar estabelecer conexão! Verifique se você está conectado a internet. Erro: {e}"
        logger.error(msg)
        print(msg)
    except Exception as e:
        msg = f"Ocorreu um erro ao tentar estabelecer conexão! Erro: {e}"
        logger.error(msg)
        print(msg)

def relogin():
    from .settings import configs

    host = os.environ.get("GWTDADOS_HOST")
    username = os.environ.get("GWTDADOS_USERNAME")
    password = os.environ.get("GWTDADOS_PASSWORD")
    configs.auth_token = asyncio.run(get_auth_token(host, username, password))


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    host = os.environ.get("GWTDADOS_HOST")
    username = os.environ.get("GWTDADOS_USERNAME")
    password = os.environ.get("GWTDADOS_PASSWORD")

    try:
        token = asyncio.run(get_auth_token(host, username, password))
        print(f"Received token: {token}")
    except Exception as e:
        print(f"Error: {e}")
