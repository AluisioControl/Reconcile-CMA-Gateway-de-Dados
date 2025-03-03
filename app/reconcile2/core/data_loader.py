import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any

import pandas as pd


class DataLoader(ABC):
    """Base para carregamento de dados"""

    @abstractmethod
    def load(self) -> pd.DataFrame:
        pass


class JsonDataLoader(DataLoader):
    """Carrega dados de arquivos JSON"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        """Carrega dados de um arquivo JSON e retorna um DataFrame."""
        with open(self.file_path) as f:
            return pd.DataFrame(json.load(f))


class GatewayDataLoader(JsonDataLoader):
    """Carrega e parseia dados de gateways"""

    def __init__(self, file_path: str, parser):
        super().__init__(file_path)
        self.parser = parser

    def load(self) -> pd.DataFrame:
        """Carrega e parseia dados de gateways de um arquivo JSON e retorna um DataFrame."""
        with open(self.file_path) as f:
            data = [self.parser(gw) for gw in json.load(f)]
            return pd.DataFrame(data)
