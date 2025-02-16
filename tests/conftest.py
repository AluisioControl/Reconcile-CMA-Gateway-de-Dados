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

registers_dnp3 = {
    "content": [
        {
            "id": "6306D364-0DEC-EF11-88FB-6045BDFE79DC",
            "name": "testador",
            "description": "retorno",
            "index": 0,
            "timeOn": 0,
            "timeOff": 0,
            "registerDataType": 0,
            "registerControlCommand": 3,
            "sensorDnp": {
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
            },
            "registerType": {
                "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
                "name": "Tipo 02",
                "active": True,
            },
            "sensorType": {
                "id": "718E03C6-D6D4-EF11-88FA-6045BDFE79DC",
                "name": "Tipo Sensor 01",
                "active": True,
            },
            "active": True,
        }
    ],
    "pagination": {
        "pageCurrent": 0,
        "pageSize": 10,
        "totalElements": 1,
        "totalPages": 1,
    },
}

registers_modbus = [
    {
        "id": "158F89BE-B025-4E93-9359-FDD0ADBD2408",
        "name": "Registrador 1",
        "description": "Descrição do registrador",
        "addressSlave": 6,
        "addressRegister": 3952,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 15,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
    {
        "id": "B6A7CB33-B4FA-47EE-93AF-44C2CCA447E4",
        "name": "Registrador 10",
        "description": "Descrição do registrador",
        "addressSlave": 2,
        "addressRegister": 2553,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 9,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
    {
        "id": "8B570EE6-7276-459C-B875-DA1A4ADA4330",
        "name": "Registrador 100",
        "description": "Descrição do registrador",
        "addressSlave": 9,
        "addressRegister": 4822,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 11,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
    {
        "id": "A7E7FCFC-CAA1-4743-9B7F-BD27EB656B56",
        "name": "Registrador 101",
        "description": "Descrição do registrador",
        "addressSlave": 9,
        "addressRegister": 3520,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 6,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
    {
        "id": "AE977982-A638-4451-9842-05CD86D30E68",
        "name": "Registrador 102",
        "description": "Descrição do registrador",
        "addressSlave": 7,
        "addressRegister": 199,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 5,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
    {
        "id": "3576D772-9298-48E3-B5EC-23E7C5DA87B8",
        "name": "Registrador 103",
        "description": "Descrição do registrador",
        "addressSlave": 1,
        "addressRegister": 1862,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 13,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
    {
        "id": "573661FA-C309-4734-AFCF-F3196B25E384",
        "name": "Registrador 104",
        "description": "Descrição do registrador",
        "addressSlave": 7,
        "addressRegister": 4937,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 4,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
    {
        "id": "6F3DC829-2BAA-4E85-B36B-8A8CBB8DEDD9",
        "name": "Registrador 105",
        "description": "Descrição do registrador",
        "addressSlave": 1,
        "addressRegister": 4682,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 3,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
    {
        "id": "45C9969E-AF1C-4C8E-A608-A7A6B25AB4B5",
        "name": "Registrador 106",
        "description": "Descrição do registrador",
        "addressSlave": 8,
        "addressRegister": 602,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 14,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
    {
        "id": "4F73BF04-4C4E-4DAA-821D-56187879E14D",
        "name": "Registrador 107",
        "description": "Descrição do registrador",
        "addressSlave": 9,
        "addressRegister": 389,
        "registerModbusType": "COIL_STATUS",
        "registerDataFormat": "TWO_BYTE_INT_UNSIGNED",
        "bit": 3,
        "multiplier": 1,
        "additive": 0,
        "active": True,
        "sensorModbus": {
            "id": "17BC1946-AF94-42AC-BC05-B6141C001272",
            "name": "Sensor 1",
        },
        "registerType": {
            "id": "DC39658D-D6D4-EF11-88FA-6045BDFE79DC",
            "name": "Tipo 02",
            "active": True,
        },
        "sensorType": {
            "id": "02D1D879-7EB2-EF11-88F8-6045BDFE79DC",
            "name": "TEM01",
            "active": True,
        },
    },
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
        "valid_register_dnp3_id": "6306D364-0DEC-EF11-88FB-6045BDFE79DC",
        "valid_register_modbus_id": "158F89BE-B025-4E93-9359-FDD0ADBD2408",
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
