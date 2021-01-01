# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
# from .models import *


# # def get_contract_data(request):
# #     contract_obj = Contract.objects.get(id = request.GET.get('contract_id'))
# #     return render(request, 'contract/partials/contract_show.html', {'contract_obj':contract_obj })


# # def update_fields_through_xeditable(request):
# #     if request.POST and request.is_ajax():
# #         data = request.POST
# #         contract_obj = Contract.objects.get( id=data['pk'] )
# #         if data['name'] in ['is_active', 'basic_salary', 'home_allowance', 'conveyance_allowance', 'professional_tax', 'medical_insurance', 'tds', 'provident_fund', 'expiry_date']:
# #             setattr(contract_obj, data['name'], data['value'])
# #         contract_obj.save()
# #     return JsonResponse({'success':1, 'action':'reload'})
