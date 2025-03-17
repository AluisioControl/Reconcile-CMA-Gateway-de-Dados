import sqlite3
import sys

def obter_tabelas(conn):
    """
    Recupera o nome de todas as tabelas de usuário (excluindo as internas do SQLite).
    """
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    return [row[0] for row in cursor.fetchall()]

def truncar_tabelas(conn):
    """
    Esvazia todas as tabelas do banco de dados.
    """
    tabelas = obter_tabelas(conn)
    cursor = conn.cursor()
    
    # Desabilita as restrições de chaves estrangeiras para evitar erros de integridade
    cursor.execute("PRAGMA foreign_keys = OFF;")
    conn.commit()
    
    for tabela in tabelas:
        try:
            print(f"Truncando a tabela '{tabela}'...")
            cursor.execute(f"DELETE FROM \"{tabela}\";")
        except sqlite3.Error as e:
            print(f"Erro ao truncar a tabela {tabela}: {e}")
    
    conn.commit()
    
    # Reativa as restrições de chaves estrangeiras
    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    print("Todas as tabelas foram truncadas com sucesso.")

def main():
    if len(sys.argv) != 2:
        print("Uso: python truncate_db.py <caminho_para_banco_de_dados>")
        sys.exit(1)
    
    db_file = sys.argv[1]
    
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        sys.exit(1)
    
    truncar_tabelas(conn)
    conn.close()

if __name__ == '__main__':
    main()
