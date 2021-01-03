from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.conf import  settings
from attendance import views
from attendance.models import Leave

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


logger = get_task_logger(__name__)

#Every month 2 date leave automatic approve
# @periodic_task(run_every=(crontab(0, 0, day_of_month='2')), name="leave_approve_every_month", ignore_result=True)
# def leave_approve_every_month():
#     logger.info("Month second date")
#     views.approve_leave_every_month()



@periodic_task(run_every=(crontab(0, 0, day_of_month='25')), name="add_rating_records", ignore_result=True)
def add_rating_records():
    from user.models import TlFeedback
    TlFeedback().generate_records()


@periodic_task(run_every=(crontab(0, 0, day_of_month='7')), name="delete_pending_rating_records", ignore_result=True)
def delete_pending_rating_records():
    from user.models import TlFeedback
    TlFeedback().delete_pending()


def send_masage_in_slack(leave):
    client = WebClient(token=settings.SLACK_BOT_TOKEN)
    try:
        text_content = render_to_string('email/leave_notification.txt', {'leave': leave,'user':leave.user})
        response = client.chat_postMessage(channel='#announcement', text=text_content)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")



@shared_task
def new_leave_email_notification(leave):
    # leave = Leave.objects.get(date=date, user=user)
    text_content = render_to_string('email/leave_notification.txt', {'leave': leave,'user':leave.user})
    html_content = render_to_string('email/leave_notification.html', {'leave': leave,'user':leave.user})
    subject = "New Leave application"
    to = [leave.user.email, leave.user.parent.email]
    send_masage_in_slack(leave)
    send_email(subject,to,text_content,html_content)


@shared_task
def leave_status_update_email_notification(leave):
    text_content = render_to_string('email/leave_notification.txt', {'leave': leave,'user':leave.user})
    html_content = render_to_string('email/leave_notification.html', {'leave': leave,'user':leave.user})
    subject = "Status Update %s"%(leave.get_status())
    to = [leave.user.email, leave.user.parent.email]
    send_email(subject,to,text_content,html_content)

@shared_task
def increment_status_update_email_notification(contract):
    text_content = render_to_string('email/increment_update_notification.txt', {'contract': contract})
    html_content = render_to_string('email/increment_update_notification.html', {'contract': contract})
    subject = "Your Salary contract update"
    to = [contract.user.email, 'yogesh@geitpl.com']
    send_email(subject,to,text_content,html_content)

# @shared_task
# def opportunity_created_email_notification(opportunity):
#     text_content = render_to_string('email/opportunity_created_notification.txt', {'opportunity': opportunity})
#     html_content = render_to_string('email/opportunity_created_notification.html', {'opportunity': opportunity})
#     subject = "New Opportunity!"
#     to = ['yogesh@geitpl.com', 'chandan@geitpl.com','diksha.v@opensoftindia.com']
#     send_email(subject,to,text_content,html_content)

def send_email(subject,to,text_content,html_content):
    msg = EmailMultiAlternatives(subject, text_content,"info@geitpl.com", to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


