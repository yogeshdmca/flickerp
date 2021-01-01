from django.conf.urls import url
from .views import *
from .ajax import *

admin = [
    url(r'^administration/opportunity/create/$', AdministrationOpportunityCreateView.as_view(), name="opportunity-create"),
    url(r'^administration/opportunity/show/(?P<pk>\d+)$', AdministrationOpportunityDetailView.as_view(), name="opportunity-show"),
    url(r'^administration/opportunities/$',AdministrationOpportunityListView.as_view(), name="opportunities"),
    url(r'^administration/lead/show/(?P<pk>\d+)$', AdministrationLeadDetailView.as_view(), name="lead-show"),
    url(r'^administration/lead/create/(?P<opportunity_id>\d+)?$', AdministrationLeadCreateView.as_view(), name="lead-create"),
    url(r'^administration/leads/$',AdministrationLeadListView.as_view(), name="leads"),
]

sales = [
    url(r'^sales/opportunity/create/$', AdministrationOpportunityCreateView.as_view(), name="sales-opportunity-create"),
    url(r'^sales/opportunity/update/(?P<pk>\d+)/$', AdministrationOpportunityUpdateView.as_view(), name="sales-opportunity-update"),
    url(r'^sales/opportunity/show/(?P<pk>\d+)/$', AdministrationOpportunityDetailView.as_view(), name="sales-opportunity-show"),
    url(r'^sales/opportunities/$',AdministrationOpportunityListView.as_view(), name="sales-opportunities"),
   
    url(r'^sales/lead/show/(?P<pk>\d+)$', AdministrationLeadDetailView.as_view(), name="sales-lead-show"),
    url(r'^sales/lead/create/(?P<opportunity_id>\d+)?$', AdministrationLeadCreateView.as_view(), name="sales-lead-create"),
    url(r'^sales/leads/$',AdministrationLeadListView.as_view(), name="sales-leads"),
]

ajax = [
    url(r'^ajax/opportunity/get-opportunity/$', get_opportunity_data, name="ajax-get-opportunity"),
    url(r'^ajax/opportunity/show-opportunity/$', show_opportunity_data, name="ajax-show-opportunity"),
    #url(r'^ajax/opportunity/update-scheduler-data/$', prospect_call_result_new, name="ajax-update-scheduler-data-opportunity"),
    url(r'^ajax/opportunity/prospect-call-result-new/(?P<pk>\d+)$', prospect_call_result_new, name="prospect-call-result-new"),

    url(r'^ajax/lead/show-opportunity/$', show_lead_data, name="ajax-show-lead"),
    url(r'^ajax/lead/update-scheduler-data/$', update_latest_schedule_lead, name="ajax-update-scheduler-data-lead"),
    url(r'^ajax/opportunity/get-client/$', get_client_data, name="ajax-get-client"),
    url(r'^ajax/opportunity/create/api/$', create_opportunity_api, name="opportunity-create-api"),
    

    

]

urlpatterns = ajax + admin + sales