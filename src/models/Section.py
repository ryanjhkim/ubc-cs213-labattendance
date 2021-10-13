COL_NUMS = 11


class Section:
    def __init__(self, status, section, activity, term, mode, interval, days, start_time, end_time, comments, is_inperson):
        self.status = status
        self.section = section
        self.activity = activity
        self.term = int(term)
        self.mode = mode
        self.interval = interval
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.comments = comments
        self.isInPerson = is_inperson

    def convert_to_db_tuple(self):
        return self.section, self.term, self.days, self.start_time, self.end_time

    def convert_to_tuple(self):
        return (self.status, self.section, self.activity, self.term, self.mode, self.interval, self.days,
                self.start_time, self.end_time, self.comments, self.isInPerson)

    def __str__(self):
        return f"\nSection {self.section} \nActivity {self.activity}\nTerm {self.term}\nDays {self.days}\n" \
               f"Start Time {self.start_time}\nEnd Time {self.end_time}\n"


def init_from_tuple(table_row):
    if len(table_row) < COL_NUMS:
        return None
    status, section, activity, term, mode, interval, days, start_time, end_time, comments, *is_inperson = table_row
    return Section(status, section, activity, term, mode, interval, days, start_time, end_time, comments, is_inperson)

