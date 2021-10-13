import requests
from bs4 import BeautifulSoup
from src.models.Section import init_from_tuple
from src.repositories.SectionDatabase import insert_section_batch, create_table_name, create_table_sql
from src.repositories.Database import get_connection, create_table
from constants import UBC_CS213_URL,

UBC_CS213_URL = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept=CPSC&course=213"
LAB = "Laboratory"

if __name__ == '__main__':
    soup = BeautifulSoup(requests.get(UBC_CS213_URL).text, "html.parser")
    section_soup = soup.find("table", "section-summary")
    cols = [header.text for header in section_soup.find_all("th")]
    rows_soup = section_soup.find_all("tr")

    print(cols)

    sections = []
    idx = 0
    term = 1
    for row in rows_soup:
        tr = [data.text.strip() for data in row.find_all("td")]
        section = init_from_tuple(tr)
        if section is not None and section.term == term and section.activity == LAB:
            if len(sections) > 0 and section.section == "":
                section.section = sections[-1].section
            sections.append(section)

    conn = get_connection()
    table_name = create_table_name(2021, 1, course_code='CPSC213', isSummer=False)
    sql = create_table_sql(2021, 1, course_code='CPSC213', isSummer=False)
    create_table(conn, sql)
    sections_db = [section.convert_to_db_tuple() for section in sections]
    insert_section_batch(conn, table_name, sections_db)



