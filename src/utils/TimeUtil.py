from datetime import datetime
import pytz
from constants import VANCOUVER_TZ, TERM_RANGE_MONTH_DAYS, SUMMER_TERM_IDX, WINTER_TERM_IDX, SUMMER_TERM_ABRV, \
    WINTER_TERM_ABRV


def get_time_in_strf(time, str_f="%Y/%m/%d %H:%M %a"):
    return time.strftime(str_f)


def get_vancouver_time_now():
    YVR = pytz.timezone(VANCOUVER_TZ)
    yvr_time = datetime.now(YVR)
    return yvr_time


def get_dates_current_year_with_month_day_range(month_day_range):
        start = get_date_current_year_with_month_day(month_day_range[0])
        end = get_date_current_year_with_month_day(month_day_range[1])
        return start, end


def get_date_current_year_with_month_day(month_day):
    return datetime.strptime(month_day, '%m/%d').date().replace(year=datetime.now().year)


def _get_term(term_ranges, time):
    for term, term_range in enumerate(term_ranges):
        term_start, term_end = get_dates_current_year_with_month_day_range(term_range)
        if term_start <= time <= term_end:
            return term
    return -1


def get_current_term():
    vancouver_date_now = get_vancouver_time_now().date()
    winter_term = _get_term(TERM_RANGE_MONTH_DAYS[WINTER_TERM_IDX], vancouver_date_now)
    if winter_term == -1:
        summer_term = _get_term(TERM_RANGE_MONTH_DAYS[SUMMER_TERM_IDX], vancouver_date_now)
        return summer_term + 1, SUMMER_TERM_ABRV
    return winter_term + 1, WINTER_TERM_ABRV


if __name__ == '__main__':
    print(get_current_term())
