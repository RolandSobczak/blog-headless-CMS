from celery import shared_task
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from .models import User

@shared_task
def send_activation_email(user: int):
    message = render_to_string('users/activation_email.html', {

    })