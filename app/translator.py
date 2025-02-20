import pandas as pd

class DataFrameTranslator:
    def __init__(self, mappings: dict):
        """
        mappings: dicionário contendo os mapeamentos de colunas para cada base.
        Exemplo:
        {
            "base1": {"coluna_original": "coluna_nova"},
            "base2": {"coluna_original": "outro_nome"}
        }
        """
        self.mappings = mappings
    
    def translate(self, df: pd.DataFrame, base: str) -> pd.DataFrame:
        """
        Traduz as colunas do DataFrame conforme o mapeamento da base fornecida.
        """
        if base not in self.mappings:
            raise ValueError(f"Base '{base}' não encontrada nos mapeamentos.")
        
        mapping = self.mappings[base]
        df_translated = df.rename(columns=mapping)
        return df_translated[list(mapping.values())]


def translate(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        """
        Traduz as colunas do DataFrame conforme o mapeamento da base fornecida.
        """
        df_translated = df.rename(columns=mapping)
        return df_translated[list(mapping.values())]

def map_fields(base_translate, base_in, base_out):
    bases = base_translate[0]  # Primeira linha contém os nomes das bases
    
    if base_in not in bases or base_out not in bases:
        raise ValueError("Base de entrada ou saída inválida")
    
    index_in = bases.index(base_in)
    index_out = bases.index(base_out)
    
    mapping = {}
    for row in base_translate[1:]:  # Pulando a primeira linha
        key = row[index_in]
        value = row[index_out]
        if key and value:  # Ignorar campos vazios
            mapping[key] = value
    
    return mapping


gateway_translate = [
    ["CMA Web","Lógica de montagem","Gateway de Dados","Banco Middlware","Import ScadaLTS","Json Rabbitmq"],
    ["ID","id_gtw","","","",""],
    ["Created At","createdAt_gtw","","","",""],
    ["Updated At","updatedAt_gtw","","","",""],
    ["User Created ID","userCreatedId_gtw","","","",""],
    ["User Updated ID","userUpdatedId_gtw","","","",""],
    ["Substation ID","substationId_gtw","","","",""],
    ["Name","name_gtw","xid_gateway","xid_gateway","","ID"],
    ["IP","ip_gtw","host","host","","IP"],
    ["Active","active_gtw","status","status","","Status"],
    ["Substation ID","id_sub","subestacao","subestacao","","Subestacao"],
    ["Substation Name","name_sub","","","",""],
    ["Substation Active","active_sub","","","",""],
    ["SAP Abbreviation","sapAbbreviation_sub","regional","regional","","Regional"],
]

hardware_translate = [
    ["CMA Web","Lógica de montagem","Gateway de Dados","Banco Middlware","Import ScadaLTS","Json Rabbitmq"],
    ["ID","id_hdw","","","",""],
    ["Created At","createdAt_hdw","","","",""],
    ["Updated At","updatedAt_hdw","","","",""],
    ["User Created ID","userCreatedId_hdw","","","",""],
    ["User Updated ID","userUpdatedId_hdw","","","",""],
    ["CMA Gateway ID","cmaGatewayId_hdw","","","",""],
    ["Name","name_hdw","","","",""],
    ["SAP ID","sapId_hdw","sap_id","sap_id","","SAP_id"],
    ["Active","active_hdw","","","",""],
    ["CMA Gateway ID","id_cma","","","",""],
    ["CMA Gateway Name","name_cma","","","",""],
    ["CMA Gateway IP","ip_cma","","","",""],
    ["CMA Gateway Active","active_cma","","","",""],
]

sensores_modbus_translate = [
    ["CMA Web","Lógica de montagem","Gateway de Dados","Banco Middlware","Import ScadaLTS","Json Rabbitmq"],
    ["ID","id_sen","xid_equip = Hardware ID+ Sensor Modbus ID","xid_equip","xid_equip","Equipamento"],
    ["Created At","createdAt_sen","","","",""],
    ["Updated At","updatedAt_sen","","","",""],
    ["User Created ID","userCreatedId_sen","","","",""],
    ["User Updated ID","userUpdatedId_sen","","","",""],
    ["Manufacturer ID","manufacturerId_sen","","","",""],
    ["Hardware ID","hardwareId_sen","","","",""],
    ["Name","name_sen","","","",""],
    ["Description","description_sen","","","",""],
    ["Model","model_sen","modelo","modelo","","Modelo"],
    ["IP","ip_sen","host","host","host","IP"],
    ["Port","port_sen","port","port","port",""],
    ["Type","type_sen","type","type","","Protocolo"],
    ["Attempts","attempts_sen","retries","retries","retries",""],
    ["Time Limit","timeLimit_sen","timeout","timeout","timeout",""],
    ["Actualization Period","actualizationPeriod_sen","updatePeriodType","updatePeriodType","updatePeriodType",""],
    ["Actualization Time","actualizationTime_sen","updatePeriods","updatePeriods","updatePeriods",""],
    ["Max Register Read","maxRegisterRead_sen","maxReadRegisterCount","maxReadRegisterCount","maxReadRegisterCount",""],
    ["Max Register Write","maxRegisterWrite_sen","maxWriteRegisterCount","maxWriteRegisterCount","maxWriteRegisterCount",""],
    ["Max Register Bits Read","maxRegisterBitsRead_sen","maxReadBitCount","maxReadBitCount","maxReadBitCount",""],
    ["Active","active_sen","enabled","enabled","enabled","Status"],
    ["Manufacturer ID","id_man","","","",""],
    ["Manufacturer Name","name_man","fabricante","fabricante","","Fabricante"],
    ["Manufacturer Active","active_man","","","",""],
    ["Hardware ID","id_hw_sen","","","",""],
    ["Hardware Name","name_hw_sen","","","",""],
    ["SAP ID","sapId_hd_sen","","","",""],
    ["Hardware Active","","","","",""],
    ["CMA Gateway ID","","","","",""],
    ["CMA Gateway Name","","","","",""],
    ["CMA Gateway IP","","","","",""],
    ["CMA Gateway Active","","","","",""],
]
sensores_dnp3_translate = [
]

registradores_modbus_translate = [
],

registradores_dnp3_translate = [
]


if __name__ == "__main__":
    # Exemplo de uso
    import json
    from app.getters.gateway import parse_gateway_data
    mapping = map_fields(
        base_translate=gateway_translate,
        base_in="Lógica de montagem",
        base_out="Json Rabbitmq"
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
