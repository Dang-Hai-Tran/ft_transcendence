# Generated by Django 5.0.2 on 2024-02-12 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backendApi', '0003_invitedcommand_invitedreason'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InvitedCommand',
            new_name='ChannelOrFriendCommand',
        ),
    ]
