from django.db.models.signals import m2m_changed
from django.conf import settings
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Mail
from .tasks import send_email
from django.core.mail import send_mail

@receiver(m2m_changed, sender=Mail.newsletters.through)
def send_email_if_created(sender, instance=None, **kwargs):
    if instance:
        content = instance.content
        if not instance.plain_text:
            content = render_to_string(instance.template, {'content': instance.content})
        newsletters_emails = [recipient.mail for recipient in instance.newsletters.all()]
        users_emails = [user.email for user in instance.users.all()]
        recipients = list(set(newsletters_emails).difference(set(users_emails)))
        send_email.delay(instance.title, content, settings.DEFAULT_FROM_EMAIL, recipients)


@receiver(m2m_changed, sender=Mail.users.through)
def send_email_if_created(sender, instance=None, **kwargs):
    if instance:
        content = instance.content
        if not instance.plain_text:
            content = render_to_string(instance.template, {'content': instance.content})
        newsletters_emails = [recipient.mail for recipient in instance.newsletters.all()]
        users_emails = [user.email for user in instance.users.all()]
        recipients = list(set(users_emails).difference(set(newsletters_emails)))
        send_email.delay(instance.title, content, settings.DEFAULT_FROM_EMAIL, recipients)
