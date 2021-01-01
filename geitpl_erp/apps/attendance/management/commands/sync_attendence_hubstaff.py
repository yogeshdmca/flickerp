from attendance.models import HubstaffUser, WorkFromHome, UserAttendanceLog, UserAttendanceLogSummary
from user.models import CustomUser
from hubstaff.client_v1 import HubstaffClient
import os
from django.core.management.base import BaseCommand
from datetime import date as datet, datetime , timedelta, time
 
class Command(BaseCommand):
    help = 'Update User Attendance Logs'

    def add_arguments(self, parser):
        parser.add_argument('--day', type=int)
        parser.add_argument('--month', type=int)
        parser.add_argument('--year', type=int)

    def handle(self, *args, **options):

        month = options['month']
        year = options['year']
        day = options['day']

        HUBSTAFF_APP_TOKEN = "S-HAXY_8ZU996f1xGEX-OATcWaAwb51HqlnwN6oi4vU"
        #hubstaff = HubstaffClient(app_token=HUBSTAFF_APP_TOKEN,username='yogesh@geitpl.com',password='Geitpl@#$123')
        #os.environ['HUBSTAFF_AUTH_TOKEN'] = hubstaff.authenticate()
        #print (os.getenv('HUBSTAFF_AUTH_TOKEN'))
        os.environ['HUBSTAFF_AUTH_TOKEN'] = "p-XSy3G4v4nkVewG0Z72G4SlDnXe8uljLzo7MJhtQ5g"

        hubstaff = HubstaffClient(app_token=HUBSTAFF_APP_TOKEN,auth_token=os.getenv('HUBSTAFF_AUTH_TOKEN'))
        hubstaff.authenticate()
        if month and year and day:
            
            params = {
                'start_date': datetime(year=year, month=month, day=day).isoformat(),
                'end_date': datetime(year=year, month=month, day=day).isoformat(),
            }
        else:
            params = {
                'start_date': datet.today().isoformat(),
                'end_date': datet.today().isoformat(),
            }

        result = hubstaff._get('/custom/by_date/team', params=params)

        for data in result['organizations'][0]['dates']:
            date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            for user in data['users']:
                #import pdb;pdb.set_trace()

                try:
                    wfh = WorkFromHome.objects.get(date=date, hubstaff_id__hubstaff_id=user['id'])
                    if user['projects']:
                        shift = wfh.user.shifts.get(date=date)
                        obj, created= UserAttendanceLog.objects.get_or_create(date=date,user=wfh.user,shift=shift)
                        #import pdb;pdb.set_trace()
                        #time_from = time(11, 30)
                        time_from = shift.shift.time_from
                        for log in user['projects']:
                            time_to = (datetime.combine(date,time_from)+timedelta(seconds=log['duration'])).time()
                            ctx = {'attendance_log':obj,
                                    'in_time':time_from,
                                    'out_time':time_to,
                                    'type':'in',
                                    'duration':timedelta(seconds=log['duration']),
                                    'comment':log['name']
                                    }
                            UserAttendanceLogSummary.objects.get_or_create(**ctx)
                            time_from = time_to
                except Exception as e:
                    print ("work from home not found", e)



