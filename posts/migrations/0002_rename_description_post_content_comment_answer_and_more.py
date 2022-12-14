# Generated by Django 4.0.6 on 2022-07-24 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='description',
            new_name='content',
        ),
        migrations.AddField(
            model_name='comment',
            name='answer',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', max_length=240, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
