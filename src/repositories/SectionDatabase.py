from src.repositories.Database import get_connection
from constants import SUMMER_TERM_ABRV, WINTER_TERM_ABRV


def insert_section_batch(connection, table_name, values):
    insert_section_sql = f"INSERT or REPLACE INTO {table_name} " \
                         f"(NAME, TERM, DAYS, START_TIME, END_TIME) VALUES (?, ?, ?, ?, ?);"
    try:
        curs = connection.cursor()
        for section in values:
            curs.execute(insert_section_sql, section)
        curs.close()
        connection.commit()
    except Exception as e:
        print(e)


def get_lab_section_by_time(table_name, time, day, connection=None):
    query_section_by_time_sql = f"SELECT * FROM {table_name} " \
                                f"WHERE START_TIME <= ? " \
                                f"AND ? <= END_TIME " \
                                f"AND DAYS = ?"
    if connection is None:
        connection = get_connection()

    try:
        curs = connection.cursor()
        curs.execute(query_section_by_time_sql, (time, time, day))
        res = curs.fetchall()
        print(res)
        return res
    except Exception as e:
        pass


def create_table_name(year, term, course_code='CPSC213', is_summer=False):
    return f"{course_code}{year}{SUMMER_TERM_ABRV if is_summer else WINTER_TERM_ABRV}{term}"


def create_table_sql(year, term, course_code='CPSC213', is_summer=False):
    table_name = create_table_name(year, term, course_code=course_code, is_summer=is_summer)
    return f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        NAME TEXT NOT NULL,
        TERM VARCHAR(1) NOT NULL,
        DAYS TEXT NOT NULL,
        START_TIME TEXT NOT NULL,
        END_TIME TEXT NOT NULL,
        PRIMARY KEY (NAME, DAYS, START_TIME, TERM)
    );
    """


