# Generated by Django 5.0.2 on 2024-02-13 18:10

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApi', '0020_alter_channel_banneds_alter_channel_inviteds_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='banneds',
            field=models.ManyToManyField(related_name='channel_banneds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='channel',
            name='inviteds',
            field=models.ManyToManyField(related_name='channel_invited', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='channel',
            name='muteds',
            field=models.ManyToManyField(related_name='channel_muteds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mutedcommand',
            name='until',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 14, 18, 10, 36, 809864, tzinfo=datetime.timezone.utc)),
        ),
    ]
