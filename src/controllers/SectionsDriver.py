"""

Main class for sections database
Run this class if first time use - ie. <ROOT OF PROJECT>/db/ is empty
Before running this class, please create a db file named cs213 (ie. cs213.db)

"""
import requests
import argparse
from bs4 import BeautifulSoup
from src.models.Section import init_from_tuple
from src.repositories.SectionDatabase import insert_section_batch, create_table_name, \
    create_table_sql, get_lab_section_by_time
from src.repositories.Database import get_connection, create_table
from constants import UBC_CS213_URL, LAB, SUMMER_TERM_ABRV
from src.utils.TimeUtil import get_vancouver_time_now, get_time_in_strf, get_current_term


def sections_cmd_parser():
    parser = argparse.ArgumentParser(description="Scrape and save CPSC 213 lab sections to local sqlite db")
    parser.add_argument('--term', '-t', choices=[1, 2], type=int,
                        help="Specifies the term of the course (1 or 2), regardless of summer or winter")
    parser.add_argument('--isSummer', '-s', type=bool,
                        help="If true, then querying summer term - else winter")
    parser.add_argument('--year', '-y', type=int,
                        help="Year")
    return parser


def get_sections(table_rows_soup, term):
    sections = []
    for row in table_rows_soup:
        tr = [data.text.strip() for data in row.find_all("td")]
        section = init_from_tuple(tr)
        if is_valid_section(section, term, activity_type=LAB):
            if len(sections) > 0 and section.section == "":
                section.section = sections[-1].section
            sections.append(section)
    return sections


def is_valid_section(section, term, activity_type=LAB):
    return section is not None and section.term == term and section.activity == activity_type


def get_current_lab_section():
    van_time = get_vancouver_time_now()
    van_time_str = get_time_in_strf(van_time)
    date, time, weekday = van_time_str.split(" ")
    year, month, day = date.split("/")
    term, term_abrv = get_current_term()
    is_summer = term_abrv == SUMMER_TERM_ABRV
    table_name = create_table_name(year, term, is_summer=is_summer)
    curr_lab_section = get_lab_section_by_time(table_name, time, weekday)
    print(curr_lab_section)
    return curr_lab_section


def setup(args_dict):
    if not all(args_dict[arg_key] is not None for arg_key in args_dict):
        raise AssertionError('1 or more required inputs were not provided values - please provide required input')
    print("Received following arguments: \n", arg_map)

    # Required Variables
    TERM = args_dict['term']
    IS_SUMMER = args_dict['isSummer']
    YEAR = args_dict['year']

    # Find relevant sections to UBC CS213 Labs
    soup = BeautifulSoup(requests.get(UBC_CS213_URL).text, "html.parser")
    section_soup = soup.find("table", "section-summary")
    rows_soup = section_soup.find_all("tr")

    # Parse table rows to local data structure
    sections = get_sections(rows_soup, args_dict['term'])

    try:
        conn = get_connection()
        table_name = create_table_name(YEAR, TERM, course_code='CPSC213', is_summer=IS_SUMMER)
        sql = create_table_sql(YEAR, TERM, course_code='CPSC213', is_summer=IS_SUMMER)
        create_table(conn, sql)
        sections_db = [section.convert_to_db_tuple() for section in sections]
        insert_section_batch(conn, table_name, sections_db)
        conn.close()
    except Exception as e:
        print("Failed to sink sections data")


if __name__ == "__main__":
    parser = sections_cmd_parser()
    args = parser.parse_args()
    arg_map = vars(args)
    setup(arg_map)
