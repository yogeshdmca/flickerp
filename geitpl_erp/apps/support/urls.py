from django.conf.urls import url
from support.views import PortfolioListView, PortfolioCreateView

employee = [
    url(r'^employee/users/portfolio/create$', PortfolioCreateView.as_view(), name="employee-portfolio-create"),
    #url(r'^employee/users/portfolio/edit$', employee.UserListView.as_view(), name="employee-portfolio-edit"),
    #url(r'^employee/users/portfolio/delete$', employee.UserListView.as_view(), name="employee-portfolio-delete"),
    url(r'^employee/users/portfolio/list$', PortfolioListView.as_view(), name="employee-portfolio-list"),
]

urlpatterns = employee