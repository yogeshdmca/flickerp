from django.contrib import admin
from .models import *
from .actions import export_as_csv_action
import copy

def copy_contract(modeladmin, request, queryset):
    # sd is an instance of SemesterDetails
    for sd in queryset:
        sd_copy = copy.copy(sd) 
        sd_copy.id = None
        sd_copy.save()

        for componant in sd.componants.all():
            componant = copy.copy(componant)
            componant.id = None
            componant.save()

            sd_copy.componants.add(componant)
            sd_copy.save()
        sd.is_active = False
        sd.save()

copy_contract.short_description = "Duplicate selected contract"

class ContractInline(admin.TabularInline):
    model = ContractComponant


class ContractAdmin(admin.ModelAdmin):
    inlines = [
        ContractInline,
    ]
    list_display = ('user', 'basic', 'hra', 'da', 'is_active')
    actions = [copy_contract]
    list_filter=('is_active',)



class PayslipLineInline(admin.TabularInline):
    model = PayslipComponant


class PaySlipAdmin(admin.ModelAdmin):
    inlines = [
        PayslipLineInline,
    ]
    list_filter=('salary_month','salary_year')
    list_display = ('user', 'salary_month', 'salary_year','office_working_days',
                    'leave_in_month','total_preset_days',
                    'get_net_salary', 'calculate_basic_gross',
                    'get_leave_deduction', 'absent_days_deduction'
                    )
    actions = [export_as_csv_action("CSV Export", fields=[
        'get_value_date', 'get_net_salary',
        'get_beneficiary_name', 'get_beneficiary_account_number',
        'get_ifsc_code', 'get_bene_email_id', 'get_bene_mobile_no',
        'get_customer_ref_no'
    ])
    ]

    actions = [export_as_csv_action("Bank Upload", fields=[
        'Transaction_Type', 'Beneficiary_Code','Value_Date',
        'Debit_AC_Number', 'Transaction_Amount','Beneficiary_Name',
        'Beneficiary_Ac_No', 'IFSC_Code', 'Bene_Email_ID','bene_Mobile_No',
        'Customer_Ref_No','Payment_Narration',
    ])
    ]



admin.site.register(Contract, ContractAdmin)
admin.site.register(PaySlip, PaySlipAdmin)
