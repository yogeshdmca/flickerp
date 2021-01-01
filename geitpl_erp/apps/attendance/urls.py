from django.conf.urls import url
from .views import *
from .ajax import *

admin = [
    url(r'^administration/attendance/list/$', AdministrationAttendanceListView.as_view(), name="attendance-list"),
    url(r'^administration/holiday/list/$', AdministrationHolidayCreateView.as_view(), name="holiday-list"),
    url(r'^administration/leaves/$', AdministrationLeaveCreateView.as_view(), name="leave"),
    url(r'^administration/leave/approve/$', CommonApproveLeaveListView.as_view(), name="approve-leave"),
    url(r'^administration/attendance/monthly-attendance/$', AdministrationMonthlyAttendanceListView.as_view(), name="administration-monthly-attendance"),
    #url(r'^administration/attendance/leave-bank/$', AdministrationLeaveBank.as_view(), name="administration-leave-bank"),
    url(r'^administration/attendance/attendance-upload/$',  attendance_upload, name="attendance-upload"),
]

common = [
    url(r'^development/attendance/list/$', CommonAttendanceListView.as_view(), name="development-attendance-list"),
    url(r'^development/holiday/list/$', CommonHolidayList.as_view(), name="development-holiday-list"),
    url(r'^development/leave/$', CommonLeaveListView.as_view(), name="development-leave"),
    url(r'^development/leave/approve/$', CommonApproveLeaveListView.as_view(), name="development-approve-leave"),
    url(r'^development/wfh/$', CommonWFHListView.as_view(), name="development-wfh"),
    # url(r'^development/leave/approve/$', CommonApproveLeaveListView.as_view(), name="development-approve-leave"),


    url(r'^sales/attendance/list/$', CommonAttendanceListView.as_view(), name="sales-attendance-list"),
    url(r'^sales/holiday/list/$', CommonHolidayList.as_view(), name="sales-holiday-list"),
    url(r'^sales/leave/$', CommonLeaveListView.as_view(), name="sales-leave"),
    url(r'^sales/approve/$', CommonApproveLeaveListView.as_view(), name="sales-approve-leave"),
]

hr = [
    url(r'^humanresource/attendance/list/$', AdministrationAttendanceListView.as_view(), name="hr-attendance-list"),
    url(r'^humanresource/holiday/list/$', AdministrationHolidayCreateView.as_view(), name="hr-holiday-list"),
    #url(r'^humanresource/leave/$', HRLeaveCreateView.as_view(), name="hr-leave"),
    #url(r'^humanresource/approve/$', HRApproveLeaveListView.as_view(), name="hr-approve-leave"),
    # url(r'^humanresource/leave/approve/$', AdministrationApproveLeaveListView.as_view(), name="humanresource-approve-leave"),
    url(r'^humanresource/attendance/monthly-attendance/$', AdministrationMonthlyAttendanceListView.as_view(), name="humanresource-monthly-attendance"),
    # url(r'^humanresource/attendance/leave-bank/$', AdministrationLeaveBank.as_view(), name="humanresource-leave-bank"),
    url(r'^humanresource/attendance/attendance-upload/$',  attendance_upload, name="humanresource-attendance-upload"),
    url(r'^humanresource/shift/list/create/$',  ShiftListCreate.as_view(), name="humanresource-shift-list-create"),
]

ajax = [
    url(r'^ajax/attendance/details/$', get_opportunity_data, name="get-attendance-detail"),
    url(r'^ajax/attendance/get-leave/$', get_leave, name="get-leave"),
    url(r'^ajax/attendance/update-leave/$', update_leave, name="update-leave"),
    url(r'^ajax/attendance/update-leave-bulk/$', update_bulk_leaves, name="update-leave-bulk"),
    url(r'^ajax/attendance/request_for_leave/$', CommonLeaveCreateView.as_view(), name="request_for_leave"),
    url(r'^ajax/attendance/request_for_leave_delete/$', request_for_leave_delete, name="request_for_leave_delete"),
    # url(r'^ajax/attendance/get_available_leave/$', get_available_leave, name="get_available_leave"),
    url(r'^ajax/attendance/add-comment/$', add_comment_for_out_punch, name="add-comment-out-punch"),
    url(r'^ajax/attendance/add-miss-punch/(?P<pk>\d+)/$', add_miss_punch, name="add-miss-punch"),
    url(r'^ajax/attendance/approve-miss-punch/$', approve_miss_punch, name="approve-miss-punch"),
    url(r'^ajax/attendance/reject-miss-punch/$', reject_miss_punch, name="reject-miss-punch"),
    url(r'^ajax/attendance/request_for_work_from_home/$', CommonWFHCreateView.as_view(), name="request_for_work_from_home"),
    url(r'^ajax/attendance/request_for_wfh_delete/$', request_for_wfh_delete, name="request_for_wfh_delete"),

]

urlpatterns = admin + ajax + common + hr
