import sqlite3

def add_column_if_not_exists(cursor, table_name, column_name, column_type):
    """
    Adiciona uma coluna à tabela se ela não existir.
    
    :param cursor: Cursor do SQLite3.
    :param table_name: Nome da tabela.
    :param column_name: Nome da coluna a ser adicionada.
    :param column_type: Tipo da coluna (ex.: INTEGER, TEXT).
    """
    # Consultar as colunas existentes na tabela
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Verificar se a coluna já existe
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        print(f"Coluna '{column_name}' adicionada à tabela '{table_name}'.")
    else:
        print(f"Coluna '{column_name}' já existe na tabela '{table_name}'.")

def migrate_database(db_path):
    """
    Executa a migração do banco de dados adicionando as colunas especificadas se não existirem.
    
    :param db_path: Caminho para o banco de dados SQLite3.
    """
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Adicionando colunas à tabela CMA_GD
    add_column_if_not_exists(cursor, "CMA_GD", "id_gtw", "INTEGER")
    add_column_if_not_exists(cursor, "CMA_GD", "id_sub", "INTEGER")

    # Adicionando colunas à tabela EQP_MODBUS_IP
    add_column_if_not_exists(cursor, "EQP_MODBUS_IP", "id_hdw", "INTEGER")
    add_column_if_not_exists(cursor, "EQP_MODBUS_IP", "name_hdw", "TEXT")
    add_column_if_not_exists(cursor, "EQP_MODBUS_IP", "type_sen", "TEXT")
    add_column_if_not_exists(cursor, "EQP_MODBUS_IP", "model_sen", "TEXT")
    add_column_if_not_exists(cursor, "EQP_MODBUS_IP", "name_sen", "TEXT")
    add_column_if_not_exists(cursor, "EQP_MODBUS_IP", "id_man", "INTEGER")

    # Adicionando colunas à tabela DP_MODBUS_IP
    add_column_if_not_exists(cursor, "DP_MODBUS_IP", "phase_reg_mod", "TEXT")
    add_column_if_not_exists(cursor, "DP_MODBUS_IP", "circuitBreakerManeuverType_reg_mod", "TEXT")
    add_column_if_not_exists(cursor, "DP_MODBUS_IP", "bushingSide", "TEXT")
    add_column_if_not_exists(cursor, "DP_MODBUS_IP", "id_reg_reg_mod", "INTEGER")
    add_column_if_not_exists(cursor, "DP_MODBUS_IP", "classificacao", "TEXT")
    add_column_if_not_exists(cursor, "DP_MODBUS_IP", "id_sen_reg_mod", "INTEGER")
    add_column_if_not_exists(cursor, "DP_MODBUS_IP", "tipo", "TEXT")

    # Confirmar as alterações e fechar a conexão
    conn.commit()
    conn.close()
    print("Migração concluída com sucesso!")

if __name__ == "__main__":
    # Caminho para o banco de dados
    db_path = "CMA_Gateway.db"
    migrate_database(db_path)