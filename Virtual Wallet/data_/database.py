# db.py
from mariadb import connect
from mariadb.connections import Connection
from common.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def _get_connection() -> Connection:
    return connect(
<<<<<<< Updated upstream
        user='root',
        password='b0t1ick0',
        host='localhost',
        port=3306,
        database='web_project'
=======
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
>>>>>>> Stashed changes
    )

def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        return list(cursor)

def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()
        return cursor.lastrowid

def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()
<<<<<<< Updated upstream

        return cursor.rowcount
=======
        return cursor.rowcount
>>>>>>> Stashed changes
