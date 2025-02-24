import asyncio

from app import getters
from app.settings import configs

print("\n")
registers_modbus = asyncio.run(
    getters.fetch_registers_modbus(
        host=configs.host, auth_token=configs.auth_token, size=1
    )
)["content"]
print(registers_modbus)
print("\n")

print("\n")
register_modbus = asyncio.run(
    getters.fetch_register_modbus_by_id(
        host=configs.host,
        auth_token=configs.auth_token,
        register_modbus_id=registers_modbus[0]["id"],
    )
)
print(register_modbus)
print("\n")
