import sqlite3
from config import Config


def conn_cursor() -> tuple[any, any] | tuple[None, None]:
    try:
        conn = sqlite3.connect(Config.DATABASE, check_same_thread=False)
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")
        return conn, cursor
    except sqlite3.Error as e:
        print(f"error making connection :{e}")
        return None, None


def create_tables(conn, cursor) -> bool:
    try:
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP NOT NULL
    )
    """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS priorities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS statuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT 
        )
        """)
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS lists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        list_id INTEGER,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        priority_id INTEGER,
        end_date TIMESTAMP,
        status_id INTEGER,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_updated TIMESTAMP,
        FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE,
        FOREIGN KEY (priority_id) REFERENCES priorities(id) ON DELETE SET NULL,
        FOREIGN KEY (status_id) REFERENCES statuses(id) ON DELETE SET NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        
        
    )
    """)
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_tags (
        task_id INTEGER,
        tag_id INTEGER,
        PRIMARY KEY ( task_id , tag_id ),
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
    )
    """)

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"error creating tables:{e}")
        return False


if __name__ == "__main__":
    conn, cursor = conn_cursor()
    if create_tables(conn, cursor):
        print("table created")
    else:
        print("tables failed")
