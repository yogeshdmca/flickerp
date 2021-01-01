from django.conf.urls import url
from service.views import employee, supervisor


administration = [
    url(r'^administration/services/$',
        supervisor.ServiceListing.as_view(), name="admin-services"),
    url(r'^administration/manageproject/$',
        supervisor.ManageProjectDaily.as_view(),
        name="admin-manage-project-daily"),
    url(r'^administration/scheduleallotment/(?P<service_id>\d+)/$',
        supervisor.ScheduleAllotment.as_view(),
        name="admin-schedule-allotment"),
    url(r'^administration/supervisor/reporting/$',
        supervisor.Reports.as_view(), name="admin-reporting"),
]


supervisor = [
    url(r'^employee/supervisor/services/$',
        supervisor.ServiceListing.as_view(), name="supervisor-services"),
    url(r'^employee/supervisor/manageproject/$',
        supervisor.ManageProjectDaily.as_view(),
        name="supervisor-manage-project-daily"),
    url(r'^employee/scheduleallotment/(?P<service_id>\d+)/$',
        supervisor.ScheduleAllotment.as_view(),
        name="supervisor-schedule-allotment"),

    url(r'^employee/supervisor/empfreebusy$',
        supervisor.EmpFreeBusy.as_view(),
        name="supervisor-emp-free-busy"),
    url(r'^employee/supervisor/service_details/(?P<pk>\d+)/$',
        supervisor.ServiceDetails.as_view(),
        name="supervisor-service-details"),

    url(r'^employee/supervisor/service_edit-x-editor/$',
        supervisor.UpdateService.as_view(),
        name="supervisor-service_edit-x-editor"),

    url(r'^employee/supervisor/service_otp/(?P<pk>\d+)/$',
        supervisor.ManageProjectTlOtp.as_view(),
        name="supervisor-service-otp"),
    url(r'^employee/supervisor/reporting/$',
        supervisor.Reports.as_view(), name="supervisor-reporting"),  

    
]

employee = [
    url(r'^employee/timehseet/$', employee.TimesheetView.as_view(),
        name="timehseet"),
    url(r'^employee/fill_timesheet/$',
        employee.FillTimesheetView.as_view(), name="employee-fill-timesheet"),
    url(r'^employee/get_timesheet_type_line/$',
        employee.get_timesheet_type_line, name="get_timesheet_type_line"),

    url(r'^employee/get_timesheet_category_type/$',
        employee.get_timesheet_category_type, name="get_timesheet_category_type"),

    url(r'^employee/get_timesheet_sub_category_type/$',
        employee.get_timesheet_sub_category_type, name="get_timesheet_sub_category_type"),
    
    url(r'^employee/add_new_timesheet_record/$',
        employee.add_new_timesheet_record, name="add_new_timesheet_record"),

    url(r'^employee/delete_timesheet_task_record/$',
        employee.delete_timesheet_task_record, name="delete_timesheet_task_record"),

    url(r'^employee/reject_timesheet/$',
        employee.RejectTimesheet.as_view(), name="employee-reject-timesheet"),

    url(r'^employee/approve_timesheet/$',
        employee.ApproveTimesheet.as_view(), name="employee-approve-timesheet"),


]


urlpatterns = supervisor + employee  +administration
