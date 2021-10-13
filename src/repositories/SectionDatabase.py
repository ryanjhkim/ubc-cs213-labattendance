def insert_section_batch(connection, table_name, values):
    insert_section_sql = f"INSERT or REPLACE INTO {table_name} (NAME, TERM, DAYS, START_TIME, END_TIME) VALUES (?, ?, ?, ?, ?);"
    try:
        curs = connection.cursor()
        for section in values:
            curs.execute(insert_section_sql, section)
        curs.close()
        connection.commit()
    except Exception as e:
        print(e)


def create_table_name(year, term, course_code='CPSC213', isSummer=False):
    return f"{course_code}{year}{'W' if isSummer else 'S'}{term}"


def create_table_sql(year, term, course_code='CPSC213', isSummer=False):
    table_name = create_table_name(year, term, course_code=course_code, isSummer=isSummer)
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


