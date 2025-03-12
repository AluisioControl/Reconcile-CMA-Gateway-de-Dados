# Coleta de dados de sensores

Esse projeto tem como objetivo coletar dados de sensores da API .... e consiliar a base do middleware com a base as informações da API.

## Pre-requisites
instale o uv (gerenciador de pacotes do python)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## install dependencies:
> Só é necessário na primeira vez ou quando houver alterações nas dependências
```bash
uv sync
```

## create .env file:
> Só é necessário na primeira vez
```bash
cp .env_sample .env
```

## coletar as informações da API do CMA_WEB
```bash
PYTHONPATH=$(pwd) uv run pythno -m app.collect_cma_web
```

## conciliar as informações coletadas com a base de dados do middleware
```bash
# reconciliar com o CMA_Gateway e o scadalts
PYTHONPATH=$(pwd) uv run python -m app.reconcile2.main
```

## conciliar as informações coletadas com a base de dados do middleware
```bash
# reconciliar com o scadalts
PYTHONPATH=$(pwd) uv run python -m app.reconcile.scadalts
# reconciliar com o cma_gateway_db
PYTHONPATH=$(pwd) uv run python -m app.reconcile.cma_gateway_db
```

## pegar o auth token: (Não necessário, só um facilitador)
```bash
PYTHONPATH=$(pwd) uv run python app/login.py
```

## rodar os tests:
```bash
PYTHONPATH=$(pwd) uv run python tests/test.py
```
