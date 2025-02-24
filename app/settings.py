import asyncio
import os

from .login import get_auth_token, relogin


class Configs:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configs, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.host = os.environ.get("GWTDADOS_HOST")
            self.username = os.environ.get("GWTDADOS_USERNAME")
            self.password = os.environ.get("GWTDADOS_PASSWORD")
            self.sqlite_db_path = os.environ.get("SQLITE_MIDDLEWARE_PATH")
            self.initialized = True

    async def login(self):
        self.auth_token = await get_auth_token(self.host, self.username, self.password)


configs = Configs()
configs.auth_token = asyncio.run(
    get_auth_token(configs.host, configs.username, configs.password)
)
configs.relogin = relogin
