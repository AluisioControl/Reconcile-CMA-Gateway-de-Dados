import os
import sqlite3  # Use o banco de sua escolha
import importlib.util
from app.settings import configs

DB_PATH = configs.sqlite_db_path

def initialize_database():
    """Inicializa a tabela de controle de migrations."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_applied_migrations():
    """Obtém a lista de migrations já aplicadas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM migrations")
    applied_migrations = {row[0] for row in cursor.fetchall()}
    conn.close()
    return applied_migrations

def mark_migration_as_applied(migration_name):
    """Marca uma migration como aplicada no banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO migrations (name) VALUES (?)", (migration_name,))
    conn.commit()
    conn.close()

def execute_migrations():
    initialize_database()
    migrations_path = os.path.join(os.path.dirname(__file__), 'migrations')
    if not os.path.exists(migrations_path):
        print(f"Migrations folder not found: {migrations_path}")
        return

    applied_migrations = get_applied_migrations()

    migration_files = sorted(
        [f for f in os.listdir(migrations_path) if f.endswith('.py') and f != '__init__.py']
    )

    for migration_file in migration_files:
        if migration_file in applied_migrations:
            print(f"Skipping already applied migration: {migration_file}")
            continue

        migration_path = os.path.join(migrations_path, migration_file)
        module_name = os.path.splitext(migration_file)[0]

        print(f"Executing migration: {migration_file}")
        # Carrega o módulo de migração
        spec = importlib.util.spec_from_file_location(module_name, migration_path)
        # Cria um novo módulo a partir do spec
        module = importlib.util.module_from_spec(spec)
        # Executa o módulo
        spec.loader.exec_module(module)
        if hasattr(module, 'run_migration'):
            module.run_migration()
        else:
            print(f"Migration file {migration_file} does not contain a run_migration function.")

        # Marca a migration como aplicada
        mark_migration_as_applied(migration_file)

if __name__ == "__main__":
    print(f"Iniciando migrações em {DB_PATH}")
    execute_migrations()