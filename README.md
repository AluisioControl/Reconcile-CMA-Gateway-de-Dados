# Coleta de dados de sensores

Esse projeto tem como objetivo coletar dados de sensores da API .... e consiliar a base do middleware com a base as informações da API.


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

## run extract:
```bash
PYTHONPATH=$(pwd) uv run reconciliation
```

## run fetch api:
```bash
PYTHONPATH=$(pwd) uv run fetch_api
```

## run reconciliation:
```bash
PYTHONPATH=$(pwd) uv run reconciliation
```




----

--Sequencia--
Steps:
 - Getways
  - Hardware
    - Sensores MODBUS
       - Resgistradores MODBUS
    - Sensores DNP
       - Resgistradores DNP

----

insert / update

delete

----

reconciliation

LOG do processo de modificações no banco de dados do middleware

----