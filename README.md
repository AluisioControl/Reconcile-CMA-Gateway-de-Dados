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


sequencia de consultas:
1. Pegar a lista de todos gateways
2. Pegar o detalhe de cada gateway
3. Pegar a lista de Hardwares de cada gateway
4. Pegar o detalhe de cada hardware
5. 1. Pegar a lista de sensores MODBUS de cada hardware (muitos devolve erro 400)
5. 2. Pegar a lista de sensores DNP3 de cada hardware (muitos devolve erro 400)
6. 1. Pegar o detalhe de cada sensor MODBUS
6. 2. Pegar o detalhe de cada sensor DNP3
7. 1. Pegar a lista de registradores MODBUS de cada sensor MODBUS
7. 2. Pegar a lista de registradores DNP3 de cada sensor DNP3
8. 1. Pegar o detalhe de cada registrador MODBUS
8. 2. Pegar o detalhe de cada registrador DNP3


----

insert / update

delete

----

reconciliation

LOG do processo de modificações no banco de dados do middleware

----