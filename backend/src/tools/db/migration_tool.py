import os
import mysql.connector
from mysql.connector import Error
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)
config = dotenv_values(env_path)

DB_CONFIG = {
    'host': config['DB_HOST'],
    'port': config['DB_PORT'],
    'user': config['DB_USER'],
    'password': config['DB_PASSWORD'],
    'database': config['DB_NAME'],
}

MIGRATIONS_PATH = 'src/db/migrations'

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f'Error connecting to MySQL: {e}')
        raise

def get_applied_migrations(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            migration_name VARCHAR(255) UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.execute('SELECT migration_name FROM migrations')
    return {row[0] for row in cursor.fetchall()}

def apply_down_migration(conn, migration_name, sql):
    cursor = conn.cursor()
    try:
        
        
        down_sql = sql.split('-- down')[1]
        for statement in down_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        print(f'Dropped table: {migration_name}')
    except Error as e:
        conn.rollback()
        print(f'Failed to Drop migration {migration_name}: {e}')

def apply_up_migration(conn, migration_name, sql):
    cursor = conn.cursor()
    try:
        up_sql = sql.split('-- down')[0]
        for statement in up_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        cursor.execute('INSERT INTO migrations (migration_name) VALUES (%s)', (migration_name,))
        conn.commit()
        print(f'Applied migration: {migration_name}')
    except Error as e:
        conn.rollback()
        print(f'Failed to apply migration {migration_name}: {e}')
        
def run_migrations():
    conn = get_db_connection()
    applied_migrations = get_applied_migrations(conn)
    
    migration_files = sorted(os.listdir(MIGRATIONS_PATH))
    # migration_files = os.listdir(MIGRATIONS_PATH)
    print(migration_files)
    # for migration_file in migration_files:
    #     if migration_file.endswith('.sql') and migration_file not in applied_migrations:
    #         with open(os.path.join(MIGRATIONS_PATH, migration_file), 'r') as file:
    #             sql = file.read()
    #         apply_down_migration(conn, migration_file, sql)
    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    for migration_file in migration_files:
        if not migration_file.startswith('_') and migration_file.endswith('.sql') and migration_file not in applied_migrations:
            with open(os.path.join(MIGRATIONS_PATH, migration_file), 'r') as file:
                sql = file.read()
            apply_up_migration(conn, migration_file, sql)
    
    conn.close()

if __name__ == '__main__':
    run_migrations()
