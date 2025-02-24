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


# TODO:
controller.py:
- [x] Coletar dados dos registros MODBUS
- [x] Combinar dados do registro MODBUS com o registro do sensor
- [x] Coletar dados dos registros DNP3
- [x] Combinar dados do registro DNP3 com o registro do sensor



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


sensor_modbus_id FC482E38-D3D8-EF11-88FA-6045BDFE79DC
sensor_modbus_id 3F80844F-A525-46A3-8F62-A7CF84B70931
sensor_modbus_id D853B4E9-84F2-494F-AB07-511FE9FE40C3
sensor_modbus_id 1E15BBB3-248D-46B7-8AFA-C79DD1C9AAA4
sensor_modbus_id DDC2E94F-E6D1-4B0F-8DA9-22BCE32E5C22
sensor_modbus_id 54903637-E00A-40E2-A00E-4106E107A002
sensor_modbus_id F0B97128-164E-4C73-8721-E78608D55014
sensor_modbus_id 08D00EF3-E0DB-4B02-B881-FFB5FCCE2F09
sensor_modbus_id AE850206-9840-4840-9FF5-8281252E24F5
sensor_modbus_id 3CAB45B6-182E-44A5-B80C-EF8C4CEBCEA3
sensor_modbus_id 17BC1946-AF94-42AC-BC05-B6141C001272
sensor_modbus_id 73455A74-02B1-4662-9DC8-070138C61EFD
sensor_modbus_id 2C1D7135-8DDB-45CD-84FB-127E0DDFB855
sensor_modbus_id 345D198D-8D16-49FF-A3AB-A897808DF651
sensor_modbus_id DE8BD179-ED21-4859-B9C1-C33FC60AF0EF
sensor_modbus_id B9A4FFEC-78B4-4A67-9E04-C920AC082710
sensor_modbus_id 2B611F1C-AAFF-4D06-A8E6-6BA1B947A0FE
sensor_modbus_id 33D50FFD-2986-4A36-A53C-74A6CE434797
sensor_modbus_id 36C1D541-9385-4054-9DD9-1E89691E3C65
sensor_modbus_id 582E1013-9C8A-438B-A662-5FAF34DA8FFA
sensor_modbus_id 5AC390AA-0113-4BAA-A78C-6DE8794E1DFB
sensor_modbus_id C6CE9078-E0D2-4B62-AF14-6CFC7C3DB220
sensor_modbus_id 19E8E660-1176-4F40-AD2B-8BDC6BDC8868
sensor_modbus_id 1AFCE0B2-8B00-477F-BAF7-6D10DBB5713D
sensor_modbus_id A7C30CC7-2CD8-4D0E-9B75-B56C9DC7902C
sensor_modbus_id 887731C9-E26A-4E55-B331-6A5BBCEC7456
sensor_modbus_id 808A9E01-4675-471A-ABF4-D8043A2E676F
sensor_modbus_id 0408D5F0-FE64-4ED3-A2CE-D8320CD7DF4B
sensor_modbus_id 472F7FC6-7809-4ED7-9F43-5E7FA2EE1844
sensor_modbus_id 13D933D9-3486-41BA-BC8F-8565E9289462
sensor_modbus_id E801DFD7-E929-4782-9FA3-12A9E71B3945
sensor_modbus_id 6D2E5157-EC45-42BD-93E5-0AF4482BA52C
sensor_modbus_id 55860E58-1AAD-44AF-8A09-2C0D794051C6
sensor_modbus_id 2319B898-0732-4CFA-837A-7557CF7F6DC9
sensor_modbus_id 2E1D500E-3430-46DF-B462-D213E2F939A8
sensor_modbus_id 337A0BED-247D-4B32-B179-593D08FA10B7
sensor_modbus_id 3F6B37BB-4718-4E25-BA64-CEC5806CD297
sensor_modbus_id A71CDD67-A9D9-4EFD-919B-8B229AE1C845
sensor_modbus_id 0B98117F-E8E4-4187-B310-26CC039B8489
sensor_modbus_id 75366380-1B0E-4146-BBCB-E61073DBF3A0
sensor_modbus_id F0078E4A-2FF8-4C5E-AF59-C20280F11F9E
sensor_modbus_id EDA7B71E-952A-405E-931E-F76098A8F4F1
sensor_modbus_id 98607FC1-55F8-4494-94AF-0727D9D73DDA
sensor_modbus_id BF9A7A37-C591-4BD5-8F23-2BF14E081ECB
sensor_modbus_id D6548865-F617-4517-A5D0-284866BE5B9A
sensor_modbus_id CD96080E-86A9-44B5-9E1F-8B90C49EA281
sensor_modbus_id 4852E408-7419-4BF1-990A-50E762C3C44D
sensor_modbus_id 2ECA458A-95D1-47BD-BFD4-F113F8A7CAFF
sensor_modbus_id 07EE9F2C-F6C4-4162-BCE2-7AC89528AA7E
sensor_modbus_id 118D0631-67BD-44E7-8364-597C957E35FC
sensor_modbus_id 622ED7AF-76B1-4E03-B934-A378A5CFBE1A
sensor_modbus_id 501CDB1E-4823-497F-A96C-9A4A42672229
sensor_modbus_id 27A42818-FD7D-4E0A-8D01-673C4AE79F48
sensor_modbus_id 2A3BEA42-10B6-43F1-8F86-846BC921E421
sensor_modbus_id FE6DBBDF-776C-463A-B729-3DD8BD661813
sensor_modbus_id B6F2CE16-8CEE-4F8D-8909-9DEE5D01B5B2
sensor_modbus_id 8FE8967D-514E-4910-989E-7B051E60C608
sensor_modbus_id 9BB1D77E-782D-4733-B926-BDEE0521CE8C
sensor_modbus_id A7A3DD46-FF15-4AF9-B27E-5BC6A096CC55
sensor_modbus_id 9B10AFBD-D42F-46A5-91F6-CAF2910BB818



# TODO - Criar um banco sqlite para armazenar os dados coletados e traduzidos para o Banco Middlware
