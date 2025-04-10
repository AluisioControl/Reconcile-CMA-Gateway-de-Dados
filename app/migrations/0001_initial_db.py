import sqlite3
from app.logger import logger

def create_database(db_path):
    """
    Cria o banco de dados inicial com todas as tabelas e índices.
    
    :param db_path: Caminho para o banco de dados SQLite3.
    """
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Criar tabela CMA_GD
    cursor.execute('''
        CREATE TABLE "CMA_GD" (
            xid_gateway VARCHAR NOT NULL, 
            subestacao VARCHAR, 
            regional VARCHAR, 
            host VARCHAR, 
            status BOOLEAN, 
            PRIMARY KEY (xid_gateway)
        )
    ''')
    cursor.execute('CREATE INDEX "ix_CMA_GD_status" ON "CMA_GD" (status)')
    cursor.execute('CREATE INDEX "ix_CMA_GD_subestacao" ON "CMA_GD" (subestacao)')
    cursor.execute('CREATE INDEX "ix_CMA_GD_xid_gateway" ON "CMA_GD" (xid_gateway)')
    cursor.execute('CREATE INDEX "ix_CMA_GD_regional" ON "CMA_GD" (regional)')
    cursor.execute('CREATE INDEX "ix_CMA_GD_host" ON "CMA_GD" (host)')

    # Criar tabela EQP_MODBUS_IP
    cursor.execute('''
        CREATE TABLE "EQP_MODBUS_IP" (
            xid_equip VARCHAR NOT NULL, 
            xid_gateway VARCHAR, 
            fabricante VARCHAR, 
            marca VARCHAR, 
            modelo VARCHAR, 
            type VARCHAR, 
            sap_id VARCHAR, 
            enabled BOOLEAN, 
            "updatePeriodType" VARCHAR, 
            "maxReadBitCount" INTEGER, 
            "maxReadRegisterCount" INTEGER, 
            "maxWriteRegisterCount" INTEGER, 
            host VARCHAR, 
            port INTEGER, 
            retries INTEGER, 
            timeout INTEGER, 
            "updatePeriods" INTEGER, 
            PRIMARY KEY (xid_equip)
        )
    ''')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_marca" ON "EQP_MODBUS_IP" (marca)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_enabled" ON "EQP_MODBUS_IP" (enabled)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_port" ON "EQP_MODBUS_IP" (port)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_modelo" ON "EQP_MODBUS_IP" (modelo)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_maxWriteRegisterCount" ON "EQP_MODBUS_IP" ("maxWriteRegisterCount")')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_xid_gateway" ON "EQP_MODBUS_IP" (xid_gateway)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_updatePeriodType" ON "EQP_MODBUS_IP" ("updatePeriodType")')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_retries" ON "EQP_MODBUS_IP" (retries)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_fabricante" ON "EQP_MODBUS_IP" (fabricante)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_type" ON "EQP_MODBUS_IP" (type)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_maxReadBitCount" ON "EQP_MODBUS_IP" ("maxReadBitCount")')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_host" ON "EQP_MODBUS_IP" (host)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_timeout" ON "EQP_MODBUS_IP" (timeout)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_sap_id" ON "EQP_MODBUS_IP" (sap_id)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_xid_equip" ON "EQP_MODBUS_IP" (xid_equip)')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_maxReadRegisterCount" ON "EQP_MODBUS_IP" ("maxReadRegisterCount")')
    cursor.execute('CREATE INDEX "ix_EQP_MODBUS_IP_updatePeriods" ON "EQP_MODBUS_IP" ("updatePeriods")')

    # Criar tabela DP_MODBUS_IP
    cursor.execute('''
        CREATE TABLE "DP_MODBUS_IP" (
            xid_sensor VARCHAR NOT NULL, 
            xid_equip VARCHAR, 
            range VARCHAR, 
            "modbusDataType" VARCHAR, 
            additive INTEGER, 
            "offset" INTEGER, 
            bit INTEGER, 
            multiplier FLOAT, 
            "slaveId" INTEGER, 
            enabled BOOLEAN, 
            nome    nome VARCHAR, 
            tipo VARCHAR, 
            classificacao VARCHAR, 
            PRIMARY KEY (xid_sensor)
        )
    ''')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_offset" ON "DP_MODBUS_IP" ("offset")')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_enabled" ON "DP_MODBUS_IP" (enabled)')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_xid_equip" ON "DP_MODBUS_IP" (xid_equip)')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_nome" ON "DP_MODBUS_IP" (nome)')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_bit" ON "DP_MODBUS_IP" (bit)')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_xid_sensor" ON "DP_MODBUS_IP" (xid_sensor)')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_additive" ON "DP_MODBUS_IP" (additive)')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_slaveId" ON "DP_MODBUS_IP" ("slaveId")')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_multiplier" ON "DP_MODBUS_IP" (multiplier)')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_tipo" ON "DP_MODBUS_IP" (tipo)')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_range" ON "DP_MODBUS_IP" (range)')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_modbusDataType" ON "DP_MODBUS_IP" ("modbusDataType")')
    cursor.execute('CREATE INDEX "ix_DP_MODBUS_IP_classificacao" ON "DP_MODBUS_IP" (classificacao)')

    # Criar tabela EQP_DNP3
    cursor.execute('''
        CREATE TABLE "EQP_DNP3" (
            xid_equip VARCHAR NOT NULL, 
            xid_gateway VARCHAR, 
            fabricante VARCHAR, 
            marca VARCHAR, 
            modelo VARCHAR, 
            type VARCHAR, 
            sap_id VARCHAR, 
            enabled BOOLEAN, 
            "eventsPeriodType" VARCHAR, 
            host VARCHAR, 
            port INTEGER, 
            "rbePollPeriods" INTEGER, 
            retries INTEGER, 
            "slaveAddress" INTEGER, 
            "sourceAddress" INTEGER, 
            "staticPollPeriods" INTEGER, 
            timeout INTEGER, 
            PRIMARY KEY (xid_equip)
        )
    ''')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_rbePollPeriods" ON "EQP_DNP3" ("rbePollPeriods")')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_staticPollPeriods" ON "EQP_DNP3" ("staticPollPeriods")')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_eventsPeriodType" ON "EQP_DNP3" ("eventsPeriodType")')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_xid_gateway" ON "EQP_DNP3" (xid_gateway)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_retries" ON "EQP_DNP3" (retries)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_type" ON "EQP_DNP3" (type)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_xid_equip" ON "EQP_DNP3" (xid_equip)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_host" ON "EQP_DNP3" (host)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_timeout" ON "EQP_DNP3" (timeout)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_slaveAddress" ON "EQP_DNP3" ("slaveAddress")')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_sap_id" ON "EQP_DNP3" (sap_id)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_port" ON "EQP_DNP3" (port)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_fabricante" ON "EQP_DNP3" (fabricante)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_marca" ON "EQP_DNP3" (marca)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_sourceAddress" ON "EQP_DNP3" ("sourceAddress")')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_enabled" ON "EQP_DNP3" (enabled)')
    cursor.execute('CREATE INDEX "ix_EQP_DNP3_modelo" ON "EQP_DNP3" (modelo)')

    # Criar tabela DP_DNP3
    cursor.execute('''
        CREATE TABLE "DP_DNP3" (
            xid_sensor VARCHAR NOT NULL, 
            xid_equip VARCHAR, 
            "dnp3DataType" INTEGER, 
            "controlCommand" INTEGER, 
            "index" INTEGER, 
            timeoff INTEGER, 
            timeon INTEGER, 
            enabled BOOLEAN, 
            nome VARCHAR, 
            tipo VARCHAR, 
            classificacao VARCHAR, 
            PRIMARY KEY (xid_sensor)
        )
    ''')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_timeoff" ON "DP_DNP3" (timeoff)')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_xid_equip" ON "DP_DNP3" (xid_equip)')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_tipo" ON "DP_DNP3" (tipo)')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_xid_sensor" ON "DP_DNP3" (xid_sensor)')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_timeon" ON "DP_DNP3" (timeon)')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_classificacao" ON "DP_DNP3" (classificacao)')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_dnp3DataType" ON "DP_DNP3" ("dnp3DataType")')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_controlCommand" ON "DP_DNP3" ("controlCommand")')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_enabled" ON "DP_DNP3" (enabled)')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_index" ON "DP_DNP3" ("index")')
    cursor.execute('CREATE INDEX "ix_DP_DNP3_nome" ON "DP_DNP3" (nome)')

    # Criar tabela EQP_TAGS
    cursor.execute('''
        CREATE TABLE "EQP_TAGS" (
            id VARCHAR NOT NULL, 
            xid_equip VARCHAR, 
            nome VARCHAR, 
            valor VARCHAR, 
            PRIMARY KEY (id)
        )
    ''')
    cursor.execute('CREATE INDEX "ix_EQP_TAGS_id" ON "EQP_TAGS" (id)')
    cursor.execute('CREATE INDEX "ix_EQP_TAGS_valor" ON "EQP_TAGS" (valor)')
    cursor.execute('CREATE INDEX "ix_EQP_TAGS_nome" ON "EQP_TAGS" (nome)')
    cursor.execute('CREATE INDEX "ix_EQP_TAGS_xid_equip" ON "EQP_TAGS" (xid_equip)')

    # Criar tabela DP_TAGS
    cursor.execute('''
        CREATE TABLE "DP_TAGS" (
            id VARCHAR NOT NULL, 
            xid_sensor VARCHAR, 
            nome VARCHAR, 
            valor VARCHAR, 
            PRIMARY KEY (id)
        )
    ''')
    cursor.execute('CREATE INDEX "ix_DP_TAGS_id" ON "DP_TAGS" (id)')
    cursor.execute('CREATE INDEX "ix_DP_TAGS_valor" ON "DP_TAGS" (valor)')
    cursor.execute('CREATE INDEX "ix_DP_TAGS_xid_sensor" ON "DP_TAGS" (xid_sensor)')
    cursor.execute('CREATE INDEX "ix_DP_TAGS_nome" ON "DP_TAGS" (nome)')

    # Criar tabela PERSISTENCE
    cursor.execute('''
        CREATE TABLE "PERSISTENCE" (
            id VARCHAR NOT NULL, 
            content_data VARCHAR, 
            sended BOOLEAN, 
            PRIMARY KEY (id)
        )
    ''')
    cursor.execute('CREATE INDEX "ix_PERSISTENCE_id" ON "PERSISTENCE" (id)')
    cursor.execute('CREATE INDEX "ix_PERSISTENCE_content_data" ON "PERSISTENCE" (content_data)')
    cursor.execute('CREATE INDEX "ix_PERSISTENCE_sended" ON "PERSISTENCE" (sended)')

    # Confirmar as alterações e fechar a conexão
    conn.commit()
    conn.close()
    logger.info("Banco de dados inicializado com sucesso!")

def run_migration():
    """
    Executa a migração do banco de dados inicial.
    """
    from app.settings import configs
    create_database(configs.sqlite_db_path)