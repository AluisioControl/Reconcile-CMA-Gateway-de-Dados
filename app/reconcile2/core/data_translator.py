from typing import Dict

import pandas as pd


class DataTranslator:
    """Traduz campos do DataFrame"""

    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping

    def translate(self, df: pd.DataFrame) -> pd.DataFrame:
        print("Mapping:", self.mapping)
        return df.rename(columns=self.mapping)
