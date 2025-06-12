import logging
import os
import pika

from dotenv import load_dotenv

if not load_dotenv():
    raise Exception("Could not load .env file")

# Localização dos arquivos de log
LOG_INFO_DEBUG = "./logs/scadalts_debug.log"
LOG_INFO_WARNING = "./logs/scadalts_info_warning.log"
LOG_ERROR = "./logs/scadalts_errors.log"

# Configurações do RabbitMQ a partir do .env
RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_PORT = int(os.getenv("RABBIT_PORT"))
RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PASS = os.getenv("RABBIT_PASS")
RABBIT_CAMINHO = os.getenv("RABBIT_CAMINHO")
RABBIT_TOPICO = os.getenv("RABBIT_TOPICO")
RABBIT_CHAVE = os.getenv("RABBIT_CHAVE")

# Configuração do formatter
log_formatter = logging.Formatter("[GATEWAY-CMA] %(asctime)s - %(levelname)s - %(funcName)s - %(message)s")


# Handler customizado para enviar mensagens ao RabbitMQ
class RabbitMQHandler(logging.Handler):
    def __init__(self, host, port, username, password, exchange, routing_key):
        super().__init__()
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(username, password)
        self.exchange = exchange
        self.routing_key = routing_key
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        try:
            # Estabelece conexão com RabbitMQ
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials)
            )
            self.channel = self.connection.channel()
            # Declara a fila com o nome do exchange (seguindo o padrão dos exemplos)
            self.channel.queue_declare(queue=self.exchange, durable=True)
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro ao conectar ao RabbitMQ ({self.host}:{self.port}): {e}")
            raise ConnectionError(f"Não foi possível conectar ao RabbitMQ: {e}")

    def emit(self, record):
        try:
            if self.connection is None or self.connection.is_closed:
                self.connect()

            # Formata a mensagem de log
            msg = self.format(record)

            # Publica a mensagem no RabbitMQ (usando exchange vazio e routing_key como nome da fila)
            self.channel.basic_publish(
                exchange='', 
                routing_key=self.exchange, 
                body=msg.encode("utf-8"), 
                properties=pika.BasicProperties(delivery_mode=2)
            )
        except Exception as e:
            print(f"Erro ao enviar mensagem para RabbitMQ: {e}")

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
        super().close()


# Carregando variáveis de ambiente
try:
    rabbit_handler = RabbitMQHandler(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        username=RABBIT_USER,
        password=RABBIT_PASS,
        exchange=RABBIT_TOPICO,
        routing_key=RABBIT_CHAVE,   
    )
    print("RabbitMQHandler configurado com sucesso.")
except Exception as e:
    print(f"Erro ao configurar RabbitMQHandler, logger não será enviado ao RabbitMQ")
    rabbit_handler = None


# Criando handlers para diferentes níveis de log
debug_handler = logging.FileHandler(LOG_INFO_WARNING)
debug_handler.setFormatter(log_formatter)
debug_handler.setLevel(logging.DEBUG)  # Aceita DEBUG

info_warning_handler = logging.FileHandler(LOG_INFO_WARNING)
info_warning_handler.setFormatter(log_formatter)
info_warning_handler.setLevel(logging.INFO)  # Aceita INFO e WARNING

error_handler = logging.FileHandler(LOG_ERROR)
error_handler.setFormatter(log_formatter)
error_handler.setLevel(logging.ERROR)  # Aceita ERROR e acima

if rabbit_handler:
    rabbit_handler.setFormatter(log_formatter)
    rabbit_handler.setLevel(logging.ERROR)  # Aceita ERROR e acima


# Filtros personalizados para segregar os níveis
class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG


class InfoWarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.INFO, logging.WARNING)


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR


# Aplicando os filtros aos handlers
debug_handler.addFilter(DebugFilter())
info_warning_handler.addFilter(InfoWarningFilter())
error_handler.addFilter(ErrorFilter())

# Configurando o logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Nível mínimo do logger (INFO para capturar tudo)

# Adicionando os handlers ao logger
logger.addHandler(debug_handler)
logger.addHandler(info_warning_handler)
logger.addHandler(error_handler)
if rabbit_handler:
    # Adiciona o handler do RabbitMQ se configurado corretamente
    logger.addHandler(rabbit_handler)


# Testando os logs
def test_logging():
    print("Testando logs...")
    logger.info("Este é um log de nível INFO")
    logger.warning("Este é um log de nível WARNING")
    logger.error("Este é um log de nível ERROR")
    logger.debug("Este é um log de nível DEBUG")
    print("Logs testados com sucesso!")


if __name__ == "__main__":
    test_logging()
