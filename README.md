# Coleta de dados de sensores

Esse projeto tem como objetivo coletar dados de sensores da API .... e consiliar a base do middleware com a base as informações da API.

## Pre-requisites
instale o uv
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

## load envs:
```bash	
export $(cat .env |grep -v ^# | xargs)
```

## get auth token:
```bash
PYTHONPATH=$(pwd) uv run python app/login.py
```

## run tests:
```bash
PYTHONPATH=$(pwd) uv run python tests/test.py
```

## coletar as informações da API do CMA_WEB
```bash
PYTHONPATH=$(pwd) uv run pythno -m app.controller
```

## conciliar as informações coletadas com a base de dados do middleware
```bash
PYTHONPATH=$(pwd) uv run python -m app.reconcile.reconciliar
```

