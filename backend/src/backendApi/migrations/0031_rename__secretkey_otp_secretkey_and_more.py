# Generated by Django 5.0.2 on 2024-02-18 10:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApi', '0030_rename_otp_otp__secretkey_remove_otp_secretkey_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otp',
            old_name='_secretKey',
            new_name='secretKey',
        ),
        migrations.AlterField(
            model_name='mutedcommand',
            name='until',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 19, 10, 54, 15, 183330, tzinfo=datetime.timezone.utc)),
        ),
    ]
