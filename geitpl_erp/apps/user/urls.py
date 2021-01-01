from django.conf.urls import url
from .views import administration, hr, employee, supervisor, common
from django.contrib.auth.decorators import login_required


from django.contrib.auth.views import logout

common = [
    url(r'^user/logout/$', logout, {'next_page': '/'}, name="logout"),
    url(r'^common/user/login/$', common.login, name="login"),
    url(r'^user/profile/$', common.UserProfileView.as_view(), name="profile"),
    url(r'^user/change-password/$',login_required(common.ChangePassword.as_view()), name="change-password"),
    url(r'^user/show_salary_password_confirm/$',common.show_salary_password_confirm, name="show_salary_password_confirm"),
    url(r'^user/yogesh/new/(?P<userid>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
        common.login_as_other, name="admin-login_as_other"),
]

admin = [
    url(r'^administration/users/$',
        administration.AdministrationUserListView.as_view(), name="admin-user-listing"),
    url(r'^administration/skill/create/$',
        administration.AdministrationSkillCreateView.as_view(), name="admin-skill-create"),
    url(r'^administration/user/create/$',
        administration.AdministrationUserCreateView.as_view(), name="admin-user-create"),
    url(r'^administration/familymember/create/$',
        administration.AdministrationFamilyMemberCreateView.as_view(), name="admin-family-member-create"),
    

]

hr = [
    url(r'^humanresource/users/$', hr.HrUserListView.as_view(), name="hr-users"),
    url(r'^humanresource/skill/create/$', hr.HrSkillCreateView.as_view(), name="hr-skill-create"),
    url(r'^humanresource/user/create/$', hr.HrUserCreateView.as_view(), name="humanresource-user-create"),
]

employee = [
    url(r'^employee/users/$', employee.UserListView.as_view(), name="employee-users"),
    url(r'^employee/get_all_events/$', employee.event_calnder, name="employee-events-view"),
    url(r'^employee/supervisor/rating/$', supervisor.TlFeedbackView.as_view(), name="employee-rating"),
    url(r'^employee/supervisor/rating-new/(?P<pk>\d+)/$', supervisor.TlFeedbackNew.as_view(), name="employee-rating-new"),
]


urlpatterns = common + admin + hr + employee
