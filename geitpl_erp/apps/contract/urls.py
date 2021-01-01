from django.conf.urls import url
from .views import *
from .ajax import *

admin = [
    url(r'^administration/contract/create/$', AdministrationContractCreateView.as_view(), name="create-contract"),
    url(r'^administration/contract/list/$', AdministrationContractListView.as_view(), name="show-contract"),
]

common = [
    url(r'^development/contract/list/$', CommonContractListView.as_view(), name="development-show-contract"),
    url(r'^development/salary-slip/(?P<pk>\d+)/$', GenerateSalarySlip.as_view(), name="generate-salary-slip"),
    url(r'^humanresource/contract/list/$', AdministrationContractListView.as_view(), name="hr-show-contract"),
	url(r'^humanresource/contract/create/$', AdministrationContractCreateView.as_view(), name="hr-create-contract"),
]

# ajax = [
#     url(r'^ajax/contract/details/$', get_contract_data, name="get-contract-detail"),
#     # url(r'^ajax/contract/update/$', update_contract, name="update-contract"),
#     url(r'^ajax/contract/update/$', update_fields_through_xeditable, name="update-fields-through-xeditable"),
# ]

urlpatterns = admin  + common
