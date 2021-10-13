import sqlite3
from constants import DB_PATH


def get_connection(sqlite_file=DB_PATH):
    connection = None
    try:
        connection = sqlite3.connect(sqlite_file)
        return connection
    except Exception as e:
        print(e)
    return connection


def create_table(conn, table_schema_sql):
    try:
        curs = conn.cursor()
        curs.execute(table_schema_sql)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    get_connection()
