# Generated by Django 5.0.3 on 2024-03-27 15:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApi', '0002_alter_mutedcommand_until'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profilePicture',
            new_name='avatarPath',
        ),
        migrations.RemoveField(
            model_name='game',
            name='maxDuration',
        ),
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('in progressing', 'In progressing'), ('end', 'End')], default='in progressing'),
        ),
        migrations.AlterField(
            model_name='mutedcommand',
            name='until',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 28, 15, 0, 35, 910136, tzinfo=datetime.timezone.utc)),
        ),
    ]
