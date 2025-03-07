import asyncio
import os

from dotenv import load_dotenv

from app.logger import logger

from .login import get_auth_token, relogin

if not load_dotenv():
    raise Exception("Could not load .env file")


class Configs:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configs, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self._auth_token = None
            self.host = os.environ.get("GWTDADOS_HOST")
            self.username = os.environ.get("GWTDADOS_USERNAME")
            self.password = os.environ.get("GWTDADOS_PASSWORD")
            self.sqlite_db_path = os.environ.get("SQLITE_MIDDLEWARE_PATH")
            self.gateway_name = os.environ.get("GATEWAY_NAME", None)
            self.DEBUG = str(os.environ.get("DEBUG", False)).lower() == "true"
            self.MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 3))
            self.MAX_PAGE_SIZE = int(os.environ.get("MAX_PAGE_SIZE", 9999))
            self.MAX_PARALLEL_REQUESTS = int(
                os.environ.get("MAX_PARALLEL_REQUESTS", 10)
            )
            self.initialized = True

    @property
    async def auth_token(self):
        if self._auth_token is None:
            self._auth_token = await get_auth_token(
                self.host, self.username, self.password
            )
        return self._auth_token

    @auth_token.setter
    async def auth_token(self, value):
        self._auth_token = value

    async def login(self):
        logger.info("Logging in...")
        self.auth_token = await get_auth_token(self.host, self.username, self.password)
        logger.info("Logged in successfully. ({})".format(self.auth_token))


configs = Configs()
configs.relogin = relogin
