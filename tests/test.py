# tests/test.py

from app.login import get_auth_token
from dotenv import load_dotenv
from pathlib import Path
from app.getters.gateways import fetch_all_gateways, fetch_gateway_by_id

def show_envs():
    print(f"GWTDADOS_HOST: {os.environ.get('GWTDADOS_HOST')}")
    print(f"GWTDADOS_USERNAME: {os.environ.get('GWTDADOS_USERNAME')}")
    print(f"GWTDADOS_PASSWORD: {os.environ.get('GWTDADOS_PASSWORD')}")

async def main():
    show_envs()
    host = "https://cma-backend-application.applications.cmapoc.com.br"  # Substitua pela URL real do host
    username = os.environ.get('GWTDADOS_USERNAME')
    password = os.environ.get('GWTDADOS_PASSWORD')
    try:
        token = await get_auth_token(host, username, password)
        os.environ['AUTH_TOKEN'] = token
        print(f"Received token: {token}")
    except Exception as e:
        print(f"Error: {e}")
    

    gateways = await fetch_all_gateways(host, token)
    print(f"Gateways: {gateways}")

if __name__ == "__main__":
    import os
    import asyncio
    # Executa o loop de eventos
    asyncio.run(main())
