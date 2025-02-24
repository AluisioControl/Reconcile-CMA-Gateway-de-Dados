# tests/test_translation.py
import pytest
import pandas as pd
from app.translator import map_fields, translate, gateway_translate  # Substitua "your_script" pelo nome do seu arquivo

# Dados de teste
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "id_gtw": [1, 2, 3],
        "name_gtw": ["gateway1", "gateway2", "gateway3"],
        "ip_gtw": ["192.168.1.1", "192.168.1.2", "192.168.1.3"],
        "active_gtw": [True, False, True],
        "extra_column": ["extra1", "extra2", "extra3"]  # Coluna extra para testar filtragem
    })

@pytest.fixture
def sample_mapping():
    return {
        "id_gtw": "ID",
        "name_gtw": "ID",
        "ip_gtw": "IP",
        "active_gtw": "Status"
    }

# Testes para map_fields
def test_map_fields_valid_bases():
    mapping = map_fields(
        base_translate=gateway_translate,
        base_in="Lógica de montagem",
        base_out="Json Rabbitmq"
    )
    assert isinstance(mapping, dict)
    assert "id_gtw" in mapping
    assert mapping["id_gtw"] == ""
    assert mapping["name_gtw"] == "ID"
    assert mapping["ip_gtw"] == "IP"

def test_map_fields_invalid_base():
    with pytest.raises(ValueError, match="Base de entrada ou saída inválida"):
        map_fields(
            base_translate=gateway_translate,
            base_in="Invalid Base",
            base_out="Json Rabbitmq"
        )

def test_map_fields_empty_fields():
    mapping = map_fields(
        base_translate=gateway_translate,
        base_in="Lógica de montagem",
        base_out="Json Rabbitmq"
    )
    # Verifica que campos vazios foram ignorados
    assert "" not in mapping.keys()
    assert "" not in mapping.values()

# Testes para translate
def test_translate_basic_functionality(sample_df, sample_mapping):
    df_translated = translate(sample_df, sample_mapping)
    
    # Verifica se as colunas foram renomeadas corretamente
    expected_columns = list(sample_mapping.values())
    assert list(df_translated.columns) == expected_columns
    
    # Verifica se os dados foram mantidos
    assert df_translated["ID"].iloc[0] == 1  # id_gtw
    assert df_translated["IP"].iloc[0] == "192.168.1.1"
    assert df_translated["Status"].iloc[0] == True

def test_translate_column_filtering(sample_df, sample_mapping):
    print(sample_mapping)
    print(sample_mapping.values())
    df_translated = translate(sample_df, sample_mapping)
    print(df_translated)
    print(df_translated.columns)
    
    # Verifica se a coluna extra foi filtrada
    assert "extra_column" in sample_df.columns
    assert "extra_column" not in df_translated.columns
    assert len(df_translated.columns) == len(sample_mapping)

def test_translate_empty_dataframe():
    empty_df = pd.DataFrame()
    mapping = {"id": "ID", "name": "Name"}
    with pytest.raises(KeyError):
        df_translated = translate(empty_df, mapping)


def test_translate_with_missing_columns(sample_df):
    mapping = {
        "id_gtw": "ID",
        "non_existent": "NonExistent"  # Coluna que não existe no DF
    }
    with pytest.raises(KeyError):
        translate(sample_df, mapping)

# Teste de integração
def test_full_translation_process():
    # Dados de exemplo
    df = pd.DataFrame({
        "id_gtw": [1],
        "name_gtw": ["test"],
        "ip_gtw": ["192.168.1.1"],
        "active_gtw": [True],
        "Subestacao": ["9.3/4"],
        "Regional": ["Sul"],
    })
    
    mapping = map_fields(
        base_translate=gateway_translate,
        base_in="Lógica de montagem",
        base_out="Json Rabbitmq"
    )
    print("mapping", mapping)
    
    df_translated = translate(df, mapping)
    
    assert "ID" in df_translated.columns
    assert "IP" in df_translated.columns
    assert "Status" in df_translated.columns
    assert df_translated["IP"].iloc[0] == "192.168.1.1"
