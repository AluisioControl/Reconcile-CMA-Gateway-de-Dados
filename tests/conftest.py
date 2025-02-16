import os
import pytest
import pytest_asyncio
from app.login import get_auth_token


HardwaresList = [
    {
        "id": "B0D0625C-AFD1-EF11-88F9-6045BDFE79DC",
        "name": "Equipamento 01",
        "sapId": "abcde",
        "active": True,
        "cmaGateway": {
            "id": "56B742EF-AED1-EF11-88F9-6045BDFE79DC",
            "name": "Gateway 01",
            "ip": "100.201.0.5",
            "active": True,
        },
    },
    {
        "id": "6FE59604-1214-48D3-A6FE-6190A38653CE",
        "name": "Equipamento 02",
        "sapId": "fghij",
        "active": True,
        "cmaGateway": {
            "id": "56B742EF-AED1-EF11-88F9-6045BDFE79DC",
            "name": "Gateway 01",
            "ip": "100.201.0.5",
            "active": True,
        },
    },
    {
        "id": "C7D3F427-BA49-4775-BC86-009BA8D9998E",
        "name": "Equipamento 03",
        "sapId": "klmno",
        "active": True,
        "cmaGateway": {
            "id": "56B742EF-AED1-EF11-88F9-6045BDFE79DC",
            "name": "Gateway 01",
            "ip": "100.201.0.5",
            "active": True,
        },
    },
    {
        "id": "3FC05D0D-9CF9-4F1C-85C7-C510F11B5C99",
        "name": "Equipamento 04",
        "sapId": "pqrst",
        "active": True,
        "cmaGateway": {
            "id": "56B742EF-AED1-EF11-88F9-6045BDFE79DC",
            "name": "Gateway 01",
            "ip": "100.201.0.5",
            "active": True,
        },
    },
    {
        "id": "0459C7C6-64BE-4552-9FE0-E7EFE42C1A14",
        "name": "Equipamento 05",
        "sapId": "uvwxy",
        "active": True,
        "cmaGateway": {
            "id": "56B742EF-AED1-EF11-88F9-6045BDFE79DC",
            "name": "Gateway 01",
            "ip": "100.201.0.5",
            "active": True,
        },
    },
    {
        "id": "C619F93C-5B0D-44DE-9711-A4AC1D70B043",
        "name": "Equipamento 06",
        "sapId": "zabcd",
        "active": False,
        "cmaGateway": {
            "id": "56B742EF-AED1-EF11-88F9-6045BDFE79DC",
            "name": "Gateway 01",
            "ip": "100.201.0.5",
            "active": True,
        },
    },
]

sensors_dnp3 = [
    {
        "id": "AF345D34-0DEC-EF11-88FB-6045BDFE79DC",
        "name": "teste",
        "description": "testando protocolo",
        "model": "xps1000",
        "ip": "192.168.55.33",
        "port": 20000,
        "type": "SENSOR",
        "attempts": 2,
        "timeLimit": 500,
        "actualizationPeriod": "MINUTES",
        "pollRbePeriod": 5,
        "pollStaticPeriod": 30,
        "addressSource": 1,
        "addressSlave": 2,
        "active": True,
        "manufacturer": {
            "id": "6917C79D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Fabricante 01",
            "active": True,
        },
        "hardware": {
            "id": "78CACAF7-0CEC-EF11-88FB-6045BDFE79DC",
            "name": "Equipamento_dnp3",
            "sapId": "10000",
        },
    }
]


@pytest_asyncio.fixture(scope="session")
async def examples():
    """Obtém o token de autenticação apenas uma vez por sessão."""
    return {
        "host": os.getenv("GWTDADOS_HOST"),
        "username": os.getenv("GWTDADOS_USERNAME"),
        "password": os.getenv("GWTDADOS_PASSWORD"),
        "valid_gateway_id": "56B742EF-AED1-EF11-88F9-6045BDFE79DC",
        "valid_hardware_id": "6FE59604-1214-48D3-A6FE-6190A38653CE",
        "valid_hardware_id_dnp3": "78CACAF7-0CEC-EF11-88FB-6045BDFE79DC",
        "valid_sensor_id": "6FE59604-1214-48D3-A6FE-6190A38653CE",
        "valid_sensor_modbus_id": "17BC1946-AF94-42AC-BC05-B6141C001272",
        "valid_sensor_dnp3_id": "AF345D34-0DEC-EF11-88FB-6045BDFE79DC",
        "hardwares": HardwaresList,
    }


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Carrega as variáveis de ambiente do .env"""
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


@pytest_asyncio.fixture(scope="session")
async def auth_token():
    """Obtém o token de autenticação apenas uma vez por sessão."""
    host = os.getenv("GWTDADOS_HOST")
    username = os.getenv("GWTDADOS_USERNAME")
    password = os.getenv("GWTDADOS_PASSWORD")

    if not all([host, username, password]):
        pytest.fail("Variáveis de ambiente necessárias não estão definidas.")

    try:
        return await get_auth_token(host, username, password)
    except Exception as e:
        pytest.fail(f"Erro ao obter token: {e}")
