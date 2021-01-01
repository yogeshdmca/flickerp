from django.conf.urls import url
from .views import *
from django.contrib.auth.views import logout
	
nouser = [
	url(r'^$', landingpage, name='landing-page'),
]

admin = [
    url(r'^administration/dashboard/$', Dashboard.as_view(), name='dashboard'),
]

common = [
    url(r'^development/dashboard/$', Dashboard.as_view(), name='development-dashboard'),
    url(r'^sales/dashboard/$', Dashboard.as_view(), name='sales-dashboard'),
    url(r'^humanresource/dashboard/$', Dashboard.as_view(), name='hr-dashboard'),
]

urlpatterns = admin +  nouser + common