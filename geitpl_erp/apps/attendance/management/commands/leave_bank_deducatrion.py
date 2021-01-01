# from contract import get_year, get_month, MONTHS
# from contract.models import PaySlip
# # from attendance.models import LeaveBank

# from django.core.management.base import BaseCommand

# class Command(BaseCommand):
#     help = 'Update User Attendance Logs'

#     def add_arguments(self, parser):
#         parser.add_argument('--user', type=int)
#         parser.add_argument('--month', type=int)
#         parser.add_argument('--year', type=int)

#     def handle(self, *args, **options):
#         #import pdb;pdb.set_trace()
#         month = options['month']
#         year = options['year']
#         user = options['user']
#         month = MONTHS[month-1][0]
#         if user:
#             salaries = PaySlip.objects.filter(salary_month = month,salary_year= year, user_id=user)
#         else:
#             salaries = PaySlip.objects.filter(salary_month = month,salary_year= year)
#         for saalry in salaries:
#             leave_in_month = eval(saalry.leave_in_month)
#             leave_in_bank = eval(saalry.leave_in_bank)
#             if leave_in_bank > leave_in_month:
#                 for leave in range(leave_in_month):
#                     LeaveBank.objects.create(user = saalry.user,type='2')
#             else:
#                 for leave in range(leave_in_bank):
#                     LeaveBank.objects.create(user = saalry.user,type='2')
