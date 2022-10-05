from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject: str, content: str, from_email: str, recipent_list: list):
    send_mail(subject, content, from_email, recipent_list)