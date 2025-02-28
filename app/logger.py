import logging
import os
import re
import time
from io import BytesIO

import pycurl
from dotenv import load_dotenv

if not load_dotenv():
    raise Exception("Could not load .env file")

# Localização dos arquivos de log
LOG_INFO_WARNING = "./logs/scadalts_info_warning.log"
LOG_ERROR = "./logs/scadalts_errors.log"

# Configuração do formatter
log_formatter = logging.Formatter(
    "[GATEWAY-CMA] %(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
)

# Criando handlers para diferentes níveis de log
info_warning_handler = logging.FileHandler(LOG_INFO_WARNING)
info_warning_handler.setFormatter(log_formatter)
info_warning_handler.setLevel(logging.INFO)  # Aceita INFO e WARNING

error_handler = logging.FileHandler(LOG_ERROR)
error_handler.setFormatter(log_formatter)
error_handler.setLevel(logging.ERROR)  # Aceita ERROR e acima


# Filtros personalizados para segregar os níveis
class InfoWarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.INFO, logging.WARNING)


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR


# Aplicando os filtros aos handlers
info_warning_handler.addFilter(InfoWarningFilter())
error_handler.addFilter(ErrorFilter())

# Configurando o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Nível mínimo do logger (INFO para capturar tudo)

# Adicionando os handlers ao logger
logger.addHandler(info_warning_handler)
logger.addHandler(error_handler)


# Testando os logs
def test_logging():
    logger.info("Este é um log de nível INFO")
    logger.warning("Este é um log de nível WARNING")
    logger.error("Este é um log de nível ERROR")


if __name__ == "__main__":
    test_logging()
