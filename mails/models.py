from django.db import models
from django.contrib.auth import get_user_model
from utils.fields import HTMLField
from utils.models import Timestamped


class Newsletter(Timestamped):
    mail = models.CharField(max_length=320, unique=True)
    is_active = models.BooleanField(default=True)


class Mail(Timestamped):
    content = HTMLField()
    template = models.FileField(upload_to='mails/templates/', null=True, blank=True)
    plain_text = models.BooleanField(default=True)
    title = models.CharField(max_length=128)
    newsletters = models.ManyToManyField(Newsletter, related_name='mails', null=True)
    users = models.ManyToManyField(get_user_model(), related_name='mails', null=True)




