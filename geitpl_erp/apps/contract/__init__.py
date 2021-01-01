from datetime import date
MONTHS = [
    ('january', 'January'),
    ('feburary', 'Feburary'),
    ('march', 'March'),
    ('april', 'April'),
    ('may', 'May'),
    ('june', 'June'),
    ('july', 'July'),
    ('august','August'),
    ('september','September'),
    ('october','October'),
    ('november','November'),
    ('december','December'),
    ]

def get_year(start_date):
    #print(start_date, start_date.month)
    return start_date.year
    if start_date.month == 1:
        return date.today().year-1
    else:
        return date.today().year

def get_month(start_date):
    month = start_date.month
    return MONTHS[month-1][0]
