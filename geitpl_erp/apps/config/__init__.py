from datetime import datetime, date, time, timedelta

TIME_LIST  = [(datetime(2018,2,2,11,30)+timedelta(minutes=30*t)).time() for t in range(1, 21) ]

TIME_SELECT = [(t, t.strftime("%H:%M %p"))for t in TIME_LIST]

SHIFT_TIME = [(datetime(2018,2,2,11,00)+timedelta(minutes=60*t)).time() for t in range(1, 9) ]

SHIFT_SELECT = [(t, t.strftime("%H:%M %p"))for t in SHIFT_TIME]


LCY=[
    (1,'Un paid'),
    (2,'Casual Leave'),
    (3,'SOL'),
    (4,'Medical'),
    (5,'Optional'),
    (6,'Menstrual'),
]

LRS=[
    (1,'Pending from TL'),
    (2,'Pending from PM'), 
    (3,'Approved'), 
    (4,'Rejected'),
    (5,'Rejected with A2'),
    (6,'Rejected with A3')
]

#Leave Requrest Type
LRT = [
    (1,'Full Day'),
    (0.5,'Half Day'), 
    (0.25,'2 hours'), 
]

LEAVE_FOR = [
    ('8','Full Day(9 hrs)'),
    ('6.5','3/4 day (6 hrs 45 min)'),
    ('5','1/2 day (4 hrs 30 min)'),
    ('2.5','1/4 day (2 hrs 15 min)'),
    ('1','1 Hour'),
    ]


LEAVE_TYPE = [('1','Casual Leave'),('3','Emergency Leave'), ('2','Optional')]


def week_range(date):
    # dow is Mon = 1, Sat = 6, Sun = 7
    year, week, dow = date.isocalendar()

    # Find the first day of the week.
    if dow == 7:
        # Since we want to start with Sunday, let's test for that condition.
        start_date = date
    else:
        # Otherwise, subtract `dow` number days to get the first day
        start_date = date - timedelta(dow)

    # Now, add 6 for the last day of the week (i.e., count up to Saturday)
    end_date = start_date + timedelta(6)

    return (start_date, end_date)


def date_range(start,end):
	dates = []
	while start<=end:
		dates.append(start)
		start = start+timedelta(days=1)
	return dates