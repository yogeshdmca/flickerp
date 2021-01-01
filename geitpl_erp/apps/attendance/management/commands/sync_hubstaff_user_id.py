from attendance.models import HubstaffUser
from user.models import CustomUser
from hubstaff.client_v1 import HubstaffClient
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Update User Attendance Logs'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        HUBSTAFF_APP_TOKEN = "S-HAXY_8ZU996f1xGEX-OATcWaAwb51HqlnwN6oi4vU"
        hubstaff = HubstaffClient(app_token=HUBSTAFF_APP_TOKEN,username='yogesh@geitpl.com',password='Geitpl@#$123')
        os.environ['HUBSTAFF_AUTH_TOKEN'] = hubstaff.authenticate()
        hubstaff = HubstaffClient(app_token=HUBSTAFF_APP_TOKEN,auth_token=os.getenv('HUBSTAFF_AUTH_TOKEN'))
        hubstaff.authenticate()
        users_list = hubstaff.get_users_list(include_projects=True,include_organizations=True)
        ids = map(lambda user: (user['id'],user['email']), users_list)
        for user_id in ids :
            try:
                user = CustomUser.objects.get(email=user_id[1])
                HubstaffUser.objects.get_or_create(user=user, hubstaff_id=user_id[0])
            except Exception as e:
                print ("user not found")
