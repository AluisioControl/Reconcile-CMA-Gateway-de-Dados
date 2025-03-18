import pandas as pd

bases_names = [
    "CMA Web old",
    "CMA Web new",
    "Lógica de montagem",
    "Gateway de Dados",
    "Banco Middlware",
    "Import ScadaLTS",
    "Json Rabbitmq",
]


def translate(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """
    Traduz as colunas do DataFrame conforme o mapeamento da base fornecida.
    """
    in_fields = list(mapping.keys())
    df_translated = df[in_fields].rename(columns=mapping)
    return df_translated


def map_fields(base_translate, base_in, base_out):

    if base_in not in bases_names:
        raise ValueError(f"Base de entrada inválida: {base_in}")
    if base_out not in bases_names:
        raise ValueError(f"Base de saída inválida: {base_out}")

    index_in = bases_names.index(base_in)
    index_out = bases_names.index(base_out)

    mapping = {}
    for row in base_translate:  # Pulando a primeira linha
        key = row[index_in]
        value = row[index_out]
        if key and value:  # Ignorar campos vazios
            mapping[key] = value
    return mapping


gateway_translate = [
    ["ID", "id", "id_gtw", "", "", "", ""],
    ["Created At", "createdAt", "createdAt_gtw", "", "", "", ""],
    ["Updated At", "updatedAt", "updatedAt_gtw", "", "", "", ""],
    ["User Created ID", "userCreatedId", "userCreatedId_gtw", "", "", "", ""],
    ["User Updated ID", "userUpdatedId", "userUpdatedId_gtw", "", "", "", ""],
    ["Substation ID", "substationId", "substationId_gtw", "", "", "", ""],
    ["Name", "name", "name_gtw", "xid_gateway", "xid_gateway", "", "ID"],
    ["IP", "ip", "ip_gtw", "host", "host", "", "IP"],
    ["Active", "active", "active_gtw", "status", "status", "", "Status"],
    ["Substation ID", "id", "id_sub", "id_sub", "id_sub", "", "id_sub"],
    [
        "Substation Name",
        "name",
        "name_sub",
        "subestacao",
        "subestacao",
        "",
        "Subestacao",
    ],
    ["Substation Active", "active", "active_sub", "", "", "", ""],
    [
        "SAP Abbreviation",
        "sapAbbreviation",
        "sapAbbreviation_sub",
        "regional",
        "regional",
        "",
        "Regional",
    ],
]
if len(gateway_translate[0]) != len(bases_names):
    raise ValueError("Número de colunas inválido para gateway_translate")

hardware_translate = [
    ["ID", "id", "id_hdw", "", "", "", ""],
    ["Created At", "createdAt", "createdAt_hdw", "", "", "", ""],
    ["Updated At", "updatedAt", "updatedAt_hdw", "", "", "", ""],
    ["User Created ID", "userCreatedId", "userCreatedId_hdw", "", "", "", ""],
    ["User Updated ID", "userUpdatedId", "userUpdatedId_hdw", "", "", "", ""],
    ["CMA Gateway ID", "cmaGatewayId", "cmaGatewayId_hdw", "", "", "", ""],
    ["Name", "name", "name_hdw", "", "", "", ""],
    ["SAP ID", "sapId", "sapId_hdw", "sap_id", "sap_id", "", "SAP_id"],
    ["", "type", "", "", "", "", ""],
    ["", "model", "", "", "", "", ""],
    ["Active", "active", "active_hdw", "", "", "", ""],
    ["CMA Gateway ID", "id", "id_cma", "", "", "", ""],
    ["CMA Gateway Name", "name", "name_cma", "", "", "", ""],
    ["CMA Gateway IP", "ip", "ip_cma", "", "", "", ""],
    ["CMA Gateway Active", "active", "active_cma", "", "", "", ""],
    ["type", "type", "type_hdw", "type", "type", "type"],
    ["model", "model", "model_hdw", "model", "model", "model"],
]
if len(hardware_translate[0]) != len(bases_names):
    raise ValueError("Número de colunas inválido para hardware_translate")


sensores_modbus_translate = [
    ["ID", "ID", "id_sen", "id_sen", "xid_equip", "xid_equip", "Equipamento"],
    ["Created At", "Created At", "createdAt_sen", "", "", "", ""],
    ["Updated At", "Updated At", "updatedAt_sen", "", "", "", ""],
    ["User Created ID", "User Created ID", "userCreatedId_sen", "", "", "", ""],
    ["User Updated ID", "User Updated ID", "userUpdatedId_sen", "", "", "", ""],
    ["Manufacturer ID", "Manufacturer ID", "manufacturerId_sen", "", "", "", ""],
    ["Hardware ID", "Hardware ID", "hardwareId_sen", "", "", "", ""],
    ["Name", "Name", "name_sen", "", "", "", ""],
    ["Description", "Description", "description_sen", "", "", "", ""],
    ["Model", "Model", "model_sen", "modelo", "modelo", "", "Modelo"],
    ["IP", "IP", "ip_sen", "host", "host", "host", "IP"],
    ["Port", "Port", "port_sen", "port", "port", "port", ""],
    ["Type", "Type", "type_sen", "type", "type", "", "Protocolo"],
    ["Attempts", "Attempts", "attempts_sen", "retries", "retries", "retries", ""],
    ["Time Limit", "Time Limit", "timeLimit_sen", "timeout", "timeout", "timeout", ""],
    [
        "Actualization Period",
        "Actualization Period",
        "actualizationPeriod_sen",
        "updatePeriodType",
        "updatePeriodType",
        "updatePeriodType",
        "",
    ],
    [
        "Actualization Time",
        "Actualization Time",
        "actualizationTime_sen",
        "updatePeriods",
        "updatePeriods",
        "updatePeriods",
        "",
    ],
    [
        "Max Register Read",
        "Max Register Read",
        "maxRegisterRead_sen",
        "maxReadRegisterCount",
        "maxReadRegisterCount",
        "maxReadRegisterCount",
        "",
    ],
    [
        "Max Register Write",
        "Max Register Write",
        "maxRegisterWrite_sen",
        "maxWriteRegisterCount",
        "maxWriteRegisterCount",
        "maxWriteRegisterCount",
        "",
    ],
    [
        "Max Register Bits Read",
        "Max Register Bits Read",
        "maxRegisterBitsRead_sen",
        "maxReadBitCount",
        "maxReadBitCount",
        "maxReadBitCount",
        "",
    ],
    ["Active", "Active", "active_sen", "enabled", "enabled", "enabled", "Status"],
    ["Manufacturer ID", "Manufacturer ID", "id_man", "", "", "", ""],
    [
        "Manufacturer Name",
        "Manufacturer Name",
        "name_man",
        "fabricante",
        "fabricante",
        "",
        "Fabricante",
    ],
    ["Manufacturer Active", "Manufacturer Active", "active_man", "", "", "", ""],
    ["Hardware ID", "id", "id_hw_sen", "", "", "", ""],
    ["Hardware Name", "name", "name_hw_sen", "", "", "", ""],
    ["SAP ID", "sapId", "sapId_hd_sen", "", "", "", ""],
    ["Hardware Active", "active", "", "", "", "", ""],
    ["", "type", "", "", "", "", ""],
    ["", "model", "", "", "", "", ""],
    ["CMA Gateway ID", "id", "", "", "", "", ""],
    ["CMA Gateway Name", "name", "", "", "", "", ""],
    ["CMA Gateway IP", "ip", "", "", "", "", ""],
    ["CMA Gateway Active", "active", "", "", "", "", ""],
    ["Manufacturer ID", "Manufacturer ID", "id_man", "id_man", "id_man", "", "id_man"],
    ["Hardware ID", "id", "id_hw_sen", "id_hw_sen", "id_hw_sen", "", "id_hw_sen"]
]
if len(sensores_modbus_translate[0]) != len(bases_names):
    raise ValueError("Número de colunas inválido para sensores_modbus_translate")


registradores_modbus_translate = [
    ["ID", "id", "id_reg_mod", "xid_sensor", "xid_sensor", "xid_sensor", "Sensor"],
    ["Created At", "createdAt", "createdAt_reg_mod", "", "", "", ""],
    ["Updated At", "updatedAt", "updatedAt_reg_mod", "", "", "", ""],
    ["User Created ID", "userCreatedId", "userCreatedId_reg_mod", "", "", "", ""],
    ["User Updated ID", "userUpdatedId", "userUpdatedId_reg_mod", "", "", "", ""],
    ["Sensor Modbus ID", "sensorModbusId", "sensorModbusId_reg_mod", "", "", "", ""],
    ["Register Type ID", "registerTypeId", "registerTypeId_reg_mod", "", "", "", ""],
    ["Sensor Type ID", "sensorTypeId", "sensorTypeId_reg_mod", "", "", "", ""],
    ["Name", "name", "name_reg_mod", "nome", "nome", "nome", "Nome"],
    ["Description", "description", "description_reg_mod", "", "", "", ""],
    [
        "Address Slave",
        "addressSlave",
        "addressSlave_reg_mod",
        "slaveId",
        "slaveId",
        "slaveId",
        "",
    ],
    [
        "Address Register",
        "addressRegister",
        "addressRegister_reg_mod",
        "offset",
        "offset",
        "offset",
        "Registrador",
    ],
    [
        "Register Modbus Type",
        "registerModbusType",
        "registerModbusType_reg_mod",
        "range",
        "range",
        "range",
        "",
    ],
    [
        "Register Data Format",
        "registerDataFormat",
        "registerDataFormat_reg_mod",
        "modbusDataType",
        "modbusDataType",
        "modbusDataType",
        "",
    ],
    ["Bit", "bit", "bit_reg_mod", "bit", "bit", "bit", ""],
    [
        "Multiplier",
        "multiplier",
        "multiplier_reg_mod",
        "multiplier",
        "multiplier",
        "multiplier",
        "",
    ],
    [
        "Additive",
        "additive",
        "additive_reg_mod",
        "additive",
        "additive",
        "additive",
        "",
    ],
    ["Active", "active", "active_reg_mod", "enabled", "enabled", "enabled", "Status"],
    ["", "phase", "", "", "", "", ""],
    ["", "circuitBreakerManeuverType", "", "", "", "", ""],
    ["", "bushingSide", "", "", "", "", ""],
    ["Sensor Modbus ID", "id", "id_sen", "", "", "", ""],
    ["Sensor Modbus Name", "name", "name_sen", "", "", "", ""],
    ["Sensor Modbus Description", "description", "description_sen", "", "", "", ""],
    ["Sensor Modbus Model", "model", "model_sen", "", "", "", ""],
    ["Sensor Modbus IP", "ip", "ip_sen", "", "", "", ""],
    ["Sensor Modbus Port", "port", "port_sen", "", "", "", ""],
    ["Sensor Modbus Type", "type", "type_sen", "", "", "", ""],
    ["Sensor Modbus Attempts", "attempts", "attempts_sen", "", "", "", ""],
    ["Sensor Modbus Time Limit", "timeLimit", "timeLimit_sen", "", "", "", ""],
    [
        "Sensor Modbus Actualization Period",
        "actualizationPeriod",
        "actualizationPeriod_sen",
        "",
        "",
        "",
        "",
    ],
    [
        "Sensor Modbus Actualization Time",
        "actualizationTime",
        "actualizationTime_sen",
        "",
        "",
        "",
        "",
    ],
    [
        "Sensor Modbus Max Register Read",
        "maxRegisterRead",
        "maxRegisterRead_sen",
        "",
        "",
        "",
        "",
    ],
    [
        "Sensor Modbus Max Register Write",
        "maxRegisterWrite",
        "maxRegisterWrite_sen",
        "",
        "",
        "",
        "",
    ],
    [
        "Sensor Modbus Max Register Bits Read",
        "maxRegisterBitsRead",
        "maxRegisterBitsRead_sen",
        "",
        "",
        "",
        "",
    ],
    ["Sensor Modbus Active", "active", "active_sen", "", "", "", ""],
    ["Sensor Modbus Manufacturer ID", "id", "id_man_reg_mod", "", "", "", ""],
    ["Sensor Modbus Manufacturer Name", "name", "name_man_reg_mod", "", "", "", ""],
    [
        "Sensor Modbus Manufacturer Active",
        "active",
        "active_man_reg_mod",
        "",
        "",
        "",
        "",
    ],
    ["Register Type ID", "id", "id_reg_reg_mod", "id_reg_reg_mod", "id_reg_reg_mod", "", "id_reg_reg_mod"],
    ["Register Type Name", "name", "name_reg_reg_mod", "tipo", "tipo", "", "Tipo"],
    ["Register Type Name", "name", "name_reg_reg_mod", "classificacao", "classificacao", "", "classificacao"],
    ["Register Type Active", "active", "active_reg_reg_mod", "", "", "", ""],
    ["Sensor Type ID", "id", "id_sen_reg_mod", "id_sen_reg_mod", "id_sen_reg_mod", "", "id_sen_reg_mod"],
    [
        "Sensor Type Name",
        "name",
        "name_sen_reg_mod",
        "tipo",
        "tipo",
        "",
        "tipo",
    ],
    ["Sensor Type Active", "active", "active_sen_reg_mod", "", "", "", ""],
]
if len(registradores_modbus_translate[0]) != len(bases_names):
    raise ValueError("Número de colunas inválido para registradores_modbus_translate")

sensores_dnp3_translate = [
    ["ID", "id", "id_reg_dnp3", "id_sen", "xid_equip ", "xid_equip ", "Equipamento"],
    ["Created At", "createdAt", "createdAt_reg_dnp3", "", "", "", ""],
    ["Updated At", "updatedAt", "updatedAt_reg_dnp3", "", "", "", ""],
    ["User Created ID", "userCreatedId", "userCreatedId_reg_dnp3", "", "", "", ""],
    ["User Updated ID", "userUpdatedId", "userUpdatedId_reg_dnp3", "", "", "", ""],
    ["Manufacturer ID", "manufacturerId", "id_man_reg_dnp3", "", "", "", ""],
    ["Hardware ID", "hardwareId", "id_dnp_reg_dnp3", "", "", "", ""],
    ["Name", "name", "name_reg_dnp3", "", "", "", ""],
    ["Description", "description", "description_reg_dnp3", "", "", "", ""],
    ["Model", "model", "model_dnp_reg_dnp3", "modelo", "modelo", "", "Modelo"],
    ["IP", "ip", "ip_dnp_reg_dnp3", "host", "host", "host", "IP"],
    ["Port", "port", "port_dnp_reg_dnp3", "port", "port", "port", ""],
    ["Type", "type", "type_dnp_reg_dnp3", "type", "type", "", "Protocolo"],
    [
        "Attempts",
        "attempts",
        "attempts_dnp_reg_dnp3",
        "retries",
        "retries",
        "retries",
        "",
    ],
    [
        "Time Limit",
        "timeLimit",
        "timeLimit_dnp_reg_dnp3",
        "timeout",
        "timeout",
        "timeout",
        "",
    ],
    [
        "Actualization Period",
        "actualizationPeriod",
        "actualizationPeriod_dnp_reg_dnp3",
        "eventsPeriodType",
        "eventsPeriodType",
        "eventsPeriodType",
        "",
    ],
    [
        "Poll RBE Period",
        "pollRbePeriod",
        "pollRbePeriod_dnp_reg_dnp3",
        "rbePollPeriods",
        "rbePollPeriods",
        "rbePollPeriods",
        "",
    ],
    [
        "Poll Static Period",
        "pollStaticPeriod",
        "pollStaticPeriod_dnp_reg_dnp3",
        "staticPollPeriods",
        "staticPollPeriods",
        "staticPollPeriods",
        "",
    ],
    [
        "Address Source",
        "addressSource",
        "addressSource_dnp_reg_dnp3",
        "sourceAddress",
        "sourceAddress",
        "sourceAddress",
        "",
    ],
    [
        "Address Slave",
        "addressSlave",
        "addressSlave_dnp_reg_dnp3",
        "slaveAddress",
        "slaveAddress",
        "slaveAddress",
        "",
    ],
    [
        "Active",
        "active",
        "active_dnp_reg_dnp3",
        "enabled",
        "enabled",
        "enabled",
        "Status",
    ],
    ["Manufacturer ID", "id", "id_man_reg_dnp3", "id_man_reg_dnp3", "id_man_reg_dnp3", "", "id_man_reg_dnp3"],
    [
        "Manufacturer Name",
        "name",
        "name_man_reg_dnp3",
        "fabricante",
        "fabricante",
        "",
        "Fabricante",
    ],
    ["Manufacturer Active", "active", "active_man_reg_mod", "", "", "", ""],
    ["Hardware ID", "id", "sensorDnpId_reg_dnp3", "sensorDnpId_reg_dnp3", "", "", "sensorDnpId_reg_dnp3"],
    ["Hardware Name", "name", "name_dnp_reg_dnp3", "", "", "", ""],
    ["SAP ID", "sapId", "sensorTypeId_reg_dnp3", "", "", "", ""],
    ["Hardware Active", "active", "active_sen_reg_dnp3", "", "", "", ""],
    ["", "type", "", "", "", "", ""],
    ["", "model", "", "", "", "", ""],
    ["CMA Gateway ID", "id", "id_sen_reg_dnp3", "", "", "", ""],
    ["CMA Gateway Name", "name", "name_sen_reg_dnp3", "", "", "", ""],
    ["CMA Gateway IP", "ip", "ip_dnp_reg_dnp3", "", "", "", ""],
    ["CMA Gateway Active", "active", "active_sen_reg_dnp3", "", "", "", ""],
]
if len(sensores_dnp3_translate[0]) != len(bases_names):
    raise ValueError("Número de colunas inválido para sensores_dnp3_translate")


registradores_dnp3_translate = [
    ["ID", "id", "id_reg_dnp3", "xid_sensor", "xid_sensor", "xid_sensor", "Sensor"],
    ["Created At", "createdAt", "createdAt_reg_dnp3", "", "", "", ""],
    ["Updated At", "updatedAt", "updatedAt_reg_dnp3", "", "", "", ""],
    ["User Created ID", "userCreatedId", "userCreatedId_reg_dnp3", "", "", "", ""],
    ["User Updated ID", "userUpdatedId", "userUpdatedId_reg_dnp3", "", "", "", ""],
    ["Sensor Dnp ID", "sensorDnpId", "sensorDnpId_reg_dnp3", "", "", "", ""],
    ["Register Type ID", "registerTypeId", "registerTypeId_reg_dnp3", "", "", "", ""],
    ["Sensor Type ID", "sensorTypeId", "sensorTypeId_reg_dnp3", "", "", "", ""],
    ["Name", "name", "name_reg_dnp3", "nome", "nome", "", "Nome"],
    [
        "Description",
        "description",
        "description_reg_dnp3",
        "classificacao",
        "classificacao",
        "",
        "",
    ],
    ["Index", "index", "index_reg_dnp3", "index", "index", "index", "Registrador"],
    ["Time On", "timeOn", "timeOn_reg_dnp3", "timeon", "timeon", "timeon", ""],
    ["Time Off", "timeOff", "timeOff_reg_dnp3", "timeoff", "timeoff", "timeoff", ""],
    [
        "Register Data Type",
        "registerDataType",
        "registerDataType_reg_dnp3",
        "dnp3DataType",
        "dnp3DataType",
        "dnp3DataType",
        "",
    ],
    [
        "Register Control Command",
        "registerControlCommand",
        "registerControlCommand_reg_dnp3",
        "controlCommand",
        "controlCommand",
        "controlCommand",
        "",
    ],
    ["Active", "active", "active_reg_dnp3", "enabled", "enabled", "enabled", "Status"],
    ["", "phase", "", "", "", "", ""],
    ["", "circuitBreakerManeuverType", "", "", "", "", ""],
    ["", "bushingSide", "", "", "", "", ""],
    ["ID", "id", "", "", "", "", ""],
    ["Name", "name", "", "", "", "", ""],
    ["Description", "description", "", "", "", "", ""],
    ["Model", "model", "", "", "", "", ""],
    ["IP", "ip", "", "", "", "", ""],
    ["Port", "port", "", "", "", "", ""],
    ["Type", "type", "", "", "", "", ""],
    ["Attempts", "attempts", "", "", "", "", ""],
    ["Time Limit", "timeLimit", "", "", "", "", ""],
    ["Actualization Period", "actualizationPeriod", "", "", "", "", ""],
    ["Poll RBE Period", "pollRbePeriod", "", "", "", "", ""],
    ["Poll Static Period", "pollStaticPeriod", "", "", "", "", ""],
    ["Address Source", "addressSource", "", "", "", "", ""],
    ["Address Slave", "addressSlave", "", "", "", "", ""],
    ["Active", "active", "", "", "", "", ""],
    ["Manufacturer ID", "id", "", "", "", "", ""],
    ["Manufacturer Name", "name", "", "", "", "", ""],
    ["Manufacturer Active", "active", "", "", "", "", ""],
    ["Register Type ID", "id", "id_reg_reg_dnp3", "id_reg_reg_dnp3", "id_reg_reg_dnp3", "id_reg_reg_dnp3", "id_reg_reg_dnp3"],
    ["Register Type Name", "name", "name_reg_reg_dnp3", "classificacao", "classificacao", "", "classificacao"],
    ["Sensor Type Name", "name", "name_sen_reg_dnp3", "tipo", "tipo", "", "Tipo"],
    ["Register Type Active", "active", "active_reg_reg_dnp_dnp3", "", "", "", ""],
    ["Sensor Type ID", "id", "id_sen_reg_dnp3", "id_sen_reg_dnp3", "id_sen_reg_dnp3", "", "id_sen_reg_dnp3"],
    [
        "Sensor Type Name",
        "name",
        "name_sen_reg_dnp3",
        "classificacao",
        "classificacao",
        "",
        "Classificacao",
    ],
    ["Sensor Type Active", "active", "active_sen_reg_dnp3", "", "", "", ""],
]
if len(registradores_dnp3_translate[0]) != len(bases_names):
    raise ValueError("Número de colunas inválido para registradores_dnp3_translate")


all_translates = gateway_translate + hardware_translate
all_translates += sensores_modbus_translate
all_translates += registradores_modbus_translate
all_translates += sensores_dnp3_translate
all_translates += registradores_dnp3_translate

if __name__ == "__main__":
    # Exemplo de uso
    import json

    from app.getters.gateway import parse_gateway_data

    mapping = map_fields(
        base_translate=gateway_translate,
        base_in="Lógica de montagem",
        base_out="Json Rabbitmq",
    )
    print("mapping:", mapping, "\n")

    with open("data.json", "r") as f:
        data = json.loads(f.read())

    # print(data[0])
    df = pd.DataFrame(data[0:3])
    in_fields = list(mapping.keys())
    out_fields = list(mapping.values())

    print("in fields:", in_fields)
    print(df[in_fields])

    print("\n")
    print("converted to: Json Rabbitmq")
    df_translated = df[in_fields].rename(columns=mapping)
    print(df_translated.to_json(lines=True, orient="records", indent=4))
