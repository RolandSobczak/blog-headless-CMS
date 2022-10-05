from django.apps import AppConfig
from django.core.signals import request_finished


class MailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mails'

    def ready(self):
        from . import signals
        request_finished.connect(signals.send_email_if_created)