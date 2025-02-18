import os

from login import get_auth_token


class App:
    def __init__(self):
        self.host = os.environ.get("GWTDADOS_HOST")
        self.username = os.environ.get("GWTDADOS_USERNAME")
        self.password = os.environ.get("GWTDADOS_PASSWORD")

    async def login(self):
        self.token = await get_auth_token(
            host=self.host, username=self.username, password=self.password
        )


if __name__ == "__main__":
    app = App()
    app.login()
