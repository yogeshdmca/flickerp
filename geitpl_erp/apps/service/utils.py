from attendance.models import this_month_start_end_date

from datetime import timedelta


def get_month_date():
    start_date, end_date, days = this_month_start_end_date()
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)
