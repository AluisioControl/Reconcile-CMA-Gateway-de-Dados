from abc import ABC, abstractmethod
from .login import get_auth_token
from app.getters.gateway import fetch_all_gateways, fetch_gateway_by_id, parse_gateway
import os

class Handler(ABC):
    def __init__(self, next_handler=None):
        self._next_handler = next_handler
        self.host = os.environ.get("GWTDADOS_HOST")
        self.username = os.environ.get("GWTDADOS_USERNAME")
        self.password = os.environ.get("GWTDADOS_PASSWORD")

    async def login(self):
        self.auth_token = await get_auth_token(
            host=self.host, username=self.username, password=self.password
        )

    @abstractmethod
    def fetch(self, data):
        pass

    @abstractmethod
    def parse(self, data):
        pass

    def next_handler(self, data):
        if self._next_handler:
            return self._next_handler.handle(data)
        return data

    def handle(self, data):
        fetched_data = self.fetch(data)
        parsed_data = self.parse(fetched_data)
        return self.next_handler(parsed_data)


class GatewayHandler(Handler):
    async def fetch(self, data):
        await self.login()
        data_gateways = fetch_all_gateways(host=self.host, auth_token=self.auth_token)
        for gateway in data_gateways:
            gateway_id = gateway["id"]
            data_gateway = await fetch_gateway_by_id(
                host=self.host, auth_token=self.auth_token, gateway_id=gateway_id
            )
            yield data_gateway

    async def parse(self, data):
        for gateway in data:
            yield parse_gateway(gateway)
        # for gateway in await self.fetch(data):
        #     yield parse_gateway(gateway)


class GatewayDetailHandler(Handler):
    def fetch(self, data):
        # Implement the logic to fetch the detail of each gateway
        pass

    def parse(self, data):
        # Implement the logic to parse the detail of each gateway
        pass


if __name__ == "__main__":
    chain = GatewayHandler()
    result = chain.handle(None)
    print(result)

