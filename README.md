# Coleta de dados de sensores

Esse projeto tem como objetivo coletar dados de sensores da API .... e consiliar a base do middleware com a base as informações da API.

## Pre-requisites
instale o uv (gerenciador de pacotes do python)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## install dependencies:
```bash
uv sync
```

## create .env file:
```bash
cp .env_sample .env
```

## load envs: (não é necessário)
```bash	
source ./loadenvs.sh
```

## pegar o auth token:
```bash
PYTHONPATH=$(pwd) uv run python app/login.py
```

## rodar os tests:
```bash
PYTHONPATH=$(pwd) uv run python tests/test.py
```

## coletar as informações da API do CMA_WEB
```bash
PYTHONPATH=$(pwd) uv run pythno -m app.controller
```

## conciliar as informações coletadas com a base de dados do middleware
```bash
# reconciliar com o scadalts
PYTHONPATH=$(pwd) uv run python -m app.reconcile.scadalts
# reconciliar com o cma_gateway_db
PYTHONPATH=$(pwd) uv run python -m app.reconcile.cma_gateway_db
```

