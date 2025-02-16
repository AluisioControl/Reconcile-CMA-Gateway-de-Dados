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
PYTHONPATH=$(pwd) uv run python -m app.controller
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


# Similarly, create other handlers for HardwareListHandler, HardwareDetailHandler, etc.

# Example usage:
# chain = GatewayListHandler(GatewayDetailHandler(HardwareListHandler(HardwareDetailHandler(...))))
# result = chain.handle(initial_data)

# quero criar uma class Collector que usará o padrão de projeto chain of responsability para coletar todos os dados necessários, para ela terá uma função de fetch que coletará o dado do elo, uma função parse onde fará a tradução dos campos e uma função next_handler para executar o elo seguinte


# perciso criar uma super tabela flat com todos os dados coletados e tratados com seus respectivos parses

# eu planejo fazer uma classes para cada tipo que receberá os dados tratados (parse) e fará a requisição para a API mutiplexando os dados coletados com os original dados


# sequencia de consultas:
# 1. Pegar a lista de todos gateways
# 2. Pegar o detalhe de cada gateway
# 3. Pegar a lista de Hardwares de cada gateway
# 4. Pegar o detalhe de cada hardware
# 5. 1. Pegar a lista de sensores MODBUS de cada hardware (muitos devolve erro 400)
# 5. 2. Pegar a lista de sensores DNP3 de cada hardware (muitos devolve erro 400)
# 6. 1. Pegar o detalhe de cada sensor MODBUS
# 6. 2. Pegar o detalhe de cada sensor DNP3
# 7. 1. Pegar a lista de registradores MODBUS de cada sensor MODBUS
# 7. 2. Pegar a lista de registradores DNP3 de cada sensor DNP3
# 8. 1. Pegar o detalhe de cada registrador MODBUS
# 8. 2. Pegar o detalhe de cada registrador DNP3
