class Command(BaseCommand):
    help = 'Update User Attendance Logs'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=int)
        parser.add_argument('--time_from', type=int)
        parser.add_argument('--time_to', type=int)

    def handle(self, *args, **options):
        user_id = options['user']
        time_from = options['time_from']
        time_to = options['time_to']

        if user_id:
            user = CustomUser.objects.filter(id=user_id)
            
        else:
            users = CustomUser.objects.all()
        if 