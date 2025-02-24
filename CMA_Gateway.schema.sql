CREATE TABLE IF NOT EXISTS "CMA_GD" (
        xid_gateway VARCHAR NOT NULL, 
        subestacao VARCHAR, 
        regional VARCHAR, 
        host VARCHAR, 
        status BOOLEAN, 
        PRIMARY KEY (xid_gateway)
);
CREATE INDEX "ix_CMA_GD_status" ON "CMA_GD" (status);
CREATE INDEX "ix_CMA_GD_subestacao" ON "CMA_GD" (subestacao);
CREATE INDEX "ix_CMA_GD_xid_gateway" ON "CMA_GD" (xid_gateway);
CREATE INDEX "ix_CMA_GD_regional" ON "CMA_GD" (regional);
CREATE INDEX "ix_CMA_GD_host" ON "CMA_GD" (host);
CREATE TABLE IF NOT EXISTS "EQP_MODBUS_IP" (
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
);
CREATE INDEX "ix_EQP_MODBUS_IP_marca" ON "EQP_MODBUS_IP" (marca);
CREATE INDEX "ix_EQP_MODBUS_IP_enabled" ON "EQP_MODBUS_IP" (enabled);
CREATE INDEX "ix_EQP_MODBUS_IP_port" ON "EQP_MODBUS_IP" (port);
CREATE INDEX "ix_EQP_MODBUS_IP_modelo" ON "EQP_MODBUS_IP" (modelo);
CREATE INDEX "ix_EQP_MODBUS_IP_maxWriteRegisterCount" ON "EQP_MODBUS_IP" ("maxWriteRegisterCount");
CREATE INDEX "ix_EQP_MODBUS_IP_xid_gateway" ON "EQP_MODBUS_IP" (xid_gateway);
CREATE INDEX "ix_EQP_MODBUS_IP_updatePeriodType" ON "EQP_MODBUS_IP" ("updatePeriodType");
CREATE INDEX "ix_EQP_MODBUS_IP_retries" ON "EQP_MODBUS_IP" (retries);
CREATE INDEX "ix_EQP_MODBUS_IP_fabricante" ON "EQP_MODBUS_IP" (fabricante);
CREATE INDEX "ix_EQP_MODBUS_IP_type" ON "EQP_MODBUS_IP" (type);
CREATE INDEX "ix_EQP_MODBUS_IP_maxReadBitCount" ON "EQP_MODBUS_IP" ("maxReadBitCount");
CREATE INDEX "ix_EQP_MODBUS_IP_host" ON "EQP_MODBUS_IP" (host);
CREATE INDEX "ix_EQP_MODBUS_IP_timeout" ON "EQP_MODBUS_IP" (timeout);
CREATE INDEX "ix_EQP_MODBUS_IP_sap_id" ON "EQP_MODBUS_IP" (sap_id);
CREATE INDEX "ix_EQP_MODBUS_IP_xid_equip" ON "EQP_MODBUS_IP" (xid_equip);
CREATE INDEX "ix_EQP_MODBUS_IP_maxReadRegisterCount" ON "EQP_MODBUS_IP" ("maxReadRegisterCount");
CREATE INDEX "ix_EQP_MODBUS_IP_updatePeriods" ON "EQP_MODBUS_IP" ("updatePeriods");
CREATE TABLE IF NOT EXISTS "DP_MODBUS_IP" (
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
        nome VARCHAR, 
        tipo VARCHAR, 
        classificacao VARCHAR, 
        PRIMARY KEY (xid_sensor)
);
CREATE INDEX "ix_DP_MODBUS_IP_offset" ON "DP_MODBUS_IP" ("offset");
CREATE INDEX "ix_DP_MODBUS_IP_enabled" ON "DP_MODBUS_IP" (enabled);
CREATE INDEX "ix_DP_MODBUS_IP_xid_equip" ON "DP_MODBUS_IP" (xid_equip);
CREATE INDEX "ix_DP_MODBUS_IP_nome" ON "DP_MODBUS_IP" (nome);
CREATE INDEX "ix_DP_MODBUS_IP_bit" ON "DP_MODBUS_IP" (bit);
CREATE INDEX "ix_DP_MODBUS_IP_xid_sensor" ON "DP_MODBUS_IP" (xid_sensor);
CREATE INDEX "ix_DP_MODBUS_IP_additive" ON "DP_MODBUS_IP" (additive);
CREATE INDEX "ix_DP_MODBUS_IP_slaveId" ON "DP_MODBUS_IP" ("slaveId");
CREATE INDEX "ix_DP_MODBUS_IP_multiplier" ON "DP_MODBUS_IP" (multiplier);
CREATE INDEX "ix_DP_MODBUS_IP_tipo" ON "DP_MODBUS_IP" (tipo);
CREATE INDEX "ix_DP_MODBUS_IP_range" ON "DP_MODBUS_IP" (range);
CREATE INDEX "ix_DP_MODBUS_IP_modbusDataType" ON "DP_MODBUS_IP" ("modbusDataType");
CREATE INDEX "ix_DP_MODBUS_IP_classificacao" ON "DP_MODBUS_IP" (classificacao);
CREATE TABLE IF NOT EXISTS "EQP_DNP3" (
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
);
CREATE INDEX "ix_EQP_DNP3_rbePollPeriods" ON "EQP_DNP3" ("rbePollPeriods");
CREATE INDEX "ix_EQP_DNP3_staticPollPeriods" ON "EQP_DNP3" ("staticPollPeriods");
CREATE INDEX "ix_EQP_DNP3_eventsPeriodType" ON "EQP_DNP3" ("eventsPeriodType");
CREATE INDEX "ix_EQP_DNP3_xid_gateway" ON "EQP_DNP3" (xid_gateway);
CREATE INDEX "ix_EQP_DNP3_retries" ON "EQP_DNP3" (retries);
CREATE INDEX "ix_EQP_DNP3_type" ON "EQP_DNP3" (type);
CREATE INDEX "ix_EQP_DNP3_xid_equip" ON "EQP_DNP3" (xid_equip);
CREATE INDEX "ix_EQP_DNP3_host" ON "EQP_DNP3" (host);
CREATE INDEX "ix_EQP_DNP3_timeout" ON "EQP_DNP3" (timeout);
CREATE INDEX "ix_EQP_DNP3_slaveAddress" ON "EQP_DNP3" ("slaveAddress");
CREATE INDEX "ix_EQP_DNP3_sap_id" ON "EQP_DNP3" (sap_id);
CREATE INDEX "ix_EQP_DNP3_port" ON "EQP_DNP3" (port);
CREATE INDEX "ix_EQP_DNP3_fabricante" ON "EQP_DNP3" (fabricante);
CREATE INDEX "ix_EQP_DNP3_marca" ON "EQP_DNP3" (marca);
CREATE INDEX "ix_EQP_DNP3_sourceAddress" ON "EQP_DNP3" ("sourceAddress");
CREATE INDEX "ix_EQP_DNP3_enabled" ON "EQP_DNP3" (enabled);
CREATE INDEX "ix_EQP_DNP3_modelo" ON "EQP_DNP3" (modelo);
CREATE TABLE IF NOT EXISTS "DP_DNP3" (
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
);
CREATE INDEX "ix_DP_DNP3_timeoff" ON "DP_DNP3" (timeoff);
CREATE INDEX "ix_DP_DNP3_xid_equip" ON "DP_DNP3" (xid_equip);
CREATE INDEX "ix_DP_DNP3_tipo" ON "DP_DNP3" (tipo);
CREATE INDEX "ix_DP_DNP3_xid_sensor" ON "DP_DNP3" (xid_sensor);
CREATE INDEX "ix_DP_DNP3_timeon" ON "DP_DNP3" (timeon);
CREATE INDEX "ix_DP_DNP3_classificacao" ON "DP_DNP3" (classificacao);
CREATE INDEX "ix_DP_DNP3_dnp3DataType" ON "DP_DNP3" ("dnp3DataType");
CREATE INDEX "ix_DP_DNP3_controlCommand" ON "DP_DNP3" ("controlCommand");
CREATE INDEX "ix_DP_DNP3_enabled" ON "DP_DNP3" (enabled);
CREATE INDEX "ix_DP_DNP3_index" ON "DP_DNP3" ("index");
CREATE INDEX "ix_DP_DNP3_nome" ON "DP_DNP3" (nome);
CREATE TABLE IF NOT EXISTS "EQP_TAGS" (
        id VARCHAR NOT NULL, 
        xid_equip VARCHAR, 
        nome VARCHAR, 
        valor VARCHAR, 
        PRIMARY KEY (id)
);
CREATE INDEX "ix_EQP_TAGS_id" ON "EQP_TAGS" (id);
CREATE INDEX "ix_EQP_TAGS_valor" ON "EQP_TAGS" (valor);
CREATE INDEX "ix_EQP_TAGS_nome" ON "EQP_TAGS" (nome);
CREATE INDEX "ix_EQP_TAGS_xid_equip" ON "EQP_TAGS" (xid_equip);
CREATE TABLE IF NOT EXISTS "DP_TAGS" (
        id VARCHAR NOT NULL, 
        xid_sensor VARCHAR, 
        nome VARCHAR, 
        valor VARCHAR, 
        PRIMARY KEY (id)
);
CREATE INDEX "ix_DP_TAGS_id" ON "DP_TAGS" (id);
CREATE INDEX "ix_DP_TAGS_valor" ON "DP_TAGS" (valor);
CREATE INDEX "ix_DP_TAGS_xid_sensor" ON "DP_TAGS" (xid_sensor);
CREATE INDEX "ix_DP_TAGS_nome" ON "DP_TAGS" (nome);
CREATE TABLE IF NOT EXISTS "PERSISTENCE" (
        id VARCHAR NOT NULL, 
        content_data VARCHAR, 
        sended BOOLEAN, 
        PRIMARY KEY (id)
);
CREATE INDEX "ix_PERSISTENCE_id" ON "PERSISTENCE" (id);
CREATE INDEX "ix_PERSISTENCE_content_data" ON "PERSISTENCE" (content_data);
CREATE INDEX "ix_PERSISTENCE_sended" ON "PERSISTENCE" (sended);