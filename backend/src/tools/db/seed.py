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


from passlib.context import CryptContext
passwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)
def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password.encode('utf8'))
    return hash


def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f'Error connecting to MySQL: {e}')
        raise


# ---- START Seeder Functions ----
def createUsers(conn):
    users = [
        ('Admin', 'admin@gmail.com', 'ADMIN', generate_password_hash('password')),
        ('User One', 'userone@gmail.com', 'USER', generate_password_hash('password')),
        ('User Two', 'usertwo@gmail.com', 'USER', generate_password_hash('password')),
    ]
    for user in users:
        sql = """
        INSERT IGNORE INTO users (name, email, role, password_hash) VALUES (%s, %s, %s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, user)
    conn.commit()

def createTasks(conn):
    
    tasks = [
        ('Initial Task', 'This is the first task', 'TODO', 'HIGH', '2024-12-31 23:59:59', None, 1, '2024-01-01 00:00:00', '2024-01-01 00:00:00'),
        ('Second Task', 'This is the second task', 'IN_PROGRESS', 'MEDIUM', '2024-11-30 23:59:59', 2, 1, '2024-02-01 00:00:00', '2024-02-01 00:00:00'),
        ('Third Task', 'This is the third task', 'DONE', 'LOW', '2024-10-31 23:59:59', 2, 1, '2024-03-01 00:00:00', '2024-03-01 00:00:00'),
        ('Fourth Task', 'This is the fourth task', 'TODO', 'HIGH', '2024-09-30 23:59:59', 2, 1, '2024-04-01 00:00:00', '2024-04-01 00:00:00'),
        ('Fifth Task', 'This is the fifth task', 'IN_PROGRESS', 'MEDIUM', '2024-08-31 23:59:59', 3, 1, '2024-05-01 00:00:00', '2024-05-01 00:00:00'),
        ('Sixth Task', 'This is the sixth task', 'DONE', 'LOW', '2024-07-31 23:59:59', 3, 1, '2024-06-01 00:00:00', '2024-06-01 00:00:00'),
    ]
    for task in tasks:
        sql = """
        INSERT IGNORE INTO tasks (title, description, status, priority, due_date, assignee_id, creator_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, task)
    conn.commit()

# ---- END Seeder Functions ----

def seed():
    conn = get_db_connection()
    
    createUsers(conn)
    createTasks(conn)
    
    conn.close()

if __name__ == '__main__':
    seed()
