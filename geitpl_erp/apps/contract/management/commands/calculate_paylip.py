from django.core.management.base import BaseCommand
# from django.forms.models import model_to_dict
from datetime import date
from user.models import CustomUser

from attendance.models import last_month_start_end_date, Leave, Holidays, UserAttendanceLog, this_month_start_end_date, month_start_end_date
from contract.models import PaySlip, PayslipComponant


from contract import MONTHS, get_year,get_month


class Command(BaseCommand):
    help = 'Update User Attendance Logs'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=int)
        parser.add_argument('--month', type=int)
        parser.add_argument('--year', type=int)

    def handle(self, *args, **options):

        month = options['month']
        year = options['year']
        user = options['user']
        if not month and year:
            raise Exception('Need to pass year and month like : --year=2019 month=6')
        start_date, end_date, number_of_days = month_start_end_date(month,year)

        users = CustomUser.objects.filter(parent__isnull=False)
        for user in users:
            salary = self.calculate_salary_lines(
                user, start_date, end_date, number_of_days)
            print salary

    def calculate_salary_lines(self, user, start_date, end_date, number_of_days):
        try:
            contract = user.contracts.get(is_active=True)
        except:
            print("No contracts created for this user")
            return {}

        BASIC = contract.basic
        HRA = contract.hra
        DA = contract.da
        ctx = [{'name': 'Basic Salary', 'amount': contract.basic,
                'type': 'BA', 'code': 'ALL'},
               {'name': 'House Rent allowance', 'amount': contract.hra,
                'type': 'HRA', 'code': 'ALL'},
               {'name': 'Daily allowances', 'amount': contract.da,
                'type': 'DA', 'code': 'ALL'},
               ]

        componants = contract.componants.all()
        for componant in componants:
            if componant.method in ['fixed', 'formula'] and eval(componant.condition):
                data = {'name': componant.name, 'amount': eval(componant.amount),
                        'type': componant.type, 'code': componant.code}
                ctx.append(data)

        # Now need to calculate working days , leave in month and leave in bank
        # before this month and save both data

        holidays = user.shifts.filter(date__range=(start_date, end_date),shift__shift_type=0).count()

        LEAVE_IN_MONTH = Leave.user_leave_count(user)
        OFFICE_WORK_DAYS = number_of_days - holidays
        LEAVE_IN_BANK = user.leave_bank
        PRESENT_DAYS = UserAttendanceLog.get_preset_days(user, start_date,end_date)

        pay_slip = {
            'contract': contract,
            'leave_in_month': LEAVE_IN_MONTH, 'office_working_days': OFFICE_WORK_DAYS,
            'leave_in_bank': user.leave_bank, 'created_by': user,
            'total_preset_days':PRESENT_DAYS
        }

        salary_month =get_month(start_date)
        salary_year  = get_year(start_date)
	print(salary_month, salary_year)
        created = PaySlip.objects.filter(
            user=user, salary_month=salary_month,salary_year = salary_year)
        print created
        if not created:
            obj, created = PaySlip.objects.get_or_create(
                user=user, salary_month=salary_month,salary_year = salary_year, **pay_slip)

            for line in ctx:
                PayslipComponant.objects.create(payslip=obj, **line)
                
        return True
