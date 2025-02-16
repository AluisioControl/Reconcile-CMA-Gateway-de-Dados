import aiohttp

class Gateway:

    def __init__(self, host, auth_token):
        """
        Args:
            host (str): URL base da API.
            auth_token (str): Token de autenticação Bearer.
        """
        self.host = host
        self.auth_token = auth_token
        self.gateways = self.process()

    async def get_gateway_by_name(self, name):
        """
        Obtém um gateway específico pelo seu nome.

        Faz uma requisição GET para o endpoint `/cma-gateways/all` a fim de recuperar a lista de gateways cadastrados.
        Em seguida, filtra a lista de gateways pelo nome especificado.

        Args:
            name (str): Nome do gateway a ser buscado.

        Returns:
            dict: Dicionário contendo informações detalhadas do gateway.

        Raises:
            Exception: Se a requisição falhar ou retornar um status diferente de 200.

        Example:
            >>> gateway = await get_gateway_by_name("https://api.example.com", "seu_token_aqui", "Gateway X")
        """
        for gateway in self.gateways:
            if gateway['name_gtw'] == name:
                return gateway
        return None

    async def fetch_all_gateways(self):
        """
        Obtém a lista de todos os gateways disponíveis.

        Faz uma requisição GET para o endpoint `/cma-gateways/all` a fim de recuperar a lista de gateways cadastrados.

        Args:
            host (str): URL base da API.
            auth_token (str): Token de autenticação Bearer.

        Returns:
            list: Lista de dicionários contendo informações dos gateways.

        Raises:
            Exception: Se a requisição falhar ou retornar um status diferente de 200.

        Example:
            >>> gateways = await fetch_all_gateways("https://api.example.com", "seu_token_aqui")
        """
        url = f"{self.host}/cma-gateways/all"
        headers = {
            'Authorization': f'Bearer {self.auth_token}'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    gateways = await response.json()
                    return gateways
                else:
                    raise Exception(f"Failed to fetch gateways, status code: {response.status}")

    @staticmethod
    def parse(data_gateway):
        """
        Converte os campos do gateway para o novo formato especificado.

        Args:
            data_gateway (dict): Dicionário com os dados originais do gateway

        Returns:
            dict: Dicionário com os campos convertidos
        """
        parsed_data = {
            "id_gtw": data_gateway.get("id", None),
            "name_gtw": data_gateway.get("name", None),
            "ip_gtw": data_gateway.get("ip", None),
            "active_gtw": data_gateway.get("active", None),
            "id_sub": data_gateway.get("substation", {}).get("id", None),
            "name_sub": data_gateway.get("substation", {}).get("name", None),
            "active_sub": data_gateway.get("substation", {}).get("active", None),
            "sapAbbreviation_sub": data_gateway.get("substation", {}).get("sapAbbreviation", None),
            "createdAt_gtw": data_gateway.get("createdAt", None),
            "updatedAt_gtw": data_gateway.get("updatedAt", None),
            "userCreatedId_gtw": data_gateway.get("userCreatedId", None),
            "userUpdatedId_gtw": data_gateway.get("userUpdatedId", None),
            "substationId_gtw": data_gateway.get("substationId", None)
        }
        return parsed_data

    async def fetch_gateway_by_id(self, gateway_id):
        """
        Obtém detalhes de um gateway específico pelo seu ID.

        Faz uma requisição GET para o endpoint `/cma-gateways/{id}` a fim de recuperar informações detalhadas de um gateway.

        Args:
            gateway_id (str): Identificador único do gateway.

        Returns:
            dict: Dicionário contendo informações detalhadas do gateway.

        Raises:
            Exception: Se a requisição falhar ou retornar um status diferente de 200.

        Example:
            >>> gateway = await fetch_gateway_by_id("https://api.example.com", "seu_token_aqui", "56B742EF-AED1-EF11-88F9-6045BDFE79DC")
        """
        url = f"{self.host}/cma-gateways/{gateway_id}"
        headers = {
            'Authorization': f'Bearer {self.auth_token}'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    gateway_info = await response.json()
                    return gateway_info
                else:
                    raise Exception(f"Failed to fetch gateway by ID, status code: {response.status}")
    
    def process(self):
        """
        Processa os gateways obtidos e os converte para o novo formato.

        Returns:
            list: Lista de dicionários contendo informações dos gateways convertidos.
        """
        parsed_gateways = []
        gateways = self.fetch_all_gateways()
        for gateway in gateways:
            data = self.fetch_gateway_by_id(gateway['id'])
            parsed_gateways.append(self.parse(data))
        return parsed_gateways
