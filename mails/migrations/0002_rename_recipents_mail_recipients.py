# Generated by Django 3.2 on 2022-09-01 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mail',
            old_name='recipents',
            new_name='recipients',
        ),
    ]