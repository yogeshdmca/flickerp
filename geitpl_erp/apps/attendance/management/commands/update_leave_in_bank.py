from django.core.management.base import BaseCommand
from attendance.models import LeaveCategory
from config.models import Year
from user.models import CustomUser
from datetime import datetime, date, timedelta

# LCY=[
#     (1,'Un paid'),
#     (2,'Casual Leave'),
#     (3,'SOL'),
#     (4,'Medical'),
#     (5,'Optional'),
#     (6,'Menstrual'),
# ]

class Command(BaseCommand):
    help = 'Update User Attendance Logs'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=int)

    def handle(self, *args, **options):
        flag = False
        user_id = options['user']
        if user_id:
            users = CustomUser.objects.filter(id=user_id)
        else:
            users = CustomUser.objects.all()
        new_year=date.today().year
        year, created = Year.objects.get_or_create(year=new_year,start=date(new_year,1,1),end=date(new_year,12,31))
        for user in users:
            if user.date_of_joining:
                if date.today().year-user.date_of_joining.year > 6:
                    LeaveCategory.objects.get_or_create(user=user,type=2,total=24,year=year)
                elif date.today().year-user.date_of_joining.year > 5:
                    LeaveCategory.objects.get_or_create(user=user,type=2,total=21,year=year)
                elif date.today().year-user.date_of_joining.year > 4:
                    LeaveCategory.objects.get_or_create(user=user,type=2,total=18,year=year)
                else:
                    LeaveCategory.objects.get_or_create(user=user,type=2,total=15,year=year)
            else:
                LeaveCategory.objects.get_or_create(user=user,type=2,total=15,year=year)
            LeaveCategory.objects.get_or_create(user=user,type=3,total=4,year=year)
            LeaveCategory.objects.get_or_create(user=user,type=4,total=5,year=year)
            LeaveCategory.objects.get_or_create(user=user,type=5,total=1,year=year)
            if user.gender=="f":
                LeaveCategory.objects.get_or_create(user=user,type=6,total=6,year=year)

            LeaveCategory.objects.get_or_create(user=user,type=1,total=24,year=year)


