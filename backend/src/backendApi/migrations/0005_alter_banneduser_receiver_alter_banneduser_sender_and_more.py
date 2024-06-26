# Generated by Django 5.0.4 on 2024-04-14 13:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApi', '0004_alter_channel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banneduser',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banneduser_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='banneduser',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banneduser_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='channel',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public'),
        ),
        migrations.AlterField(
            model_name='channelbanneduser',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channelbanneduser_channel', to='backendApi.channel'),
        ),
        migrations.AlterField(
            model_name='channelbanneduser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channelbanneduser_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='channelinviteduser',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channelinviteduser_channel', to='backendApi.channel'),
        ),
        migrations.AlterField(
            model_name='channelinviteduser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channelinviteduser_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='channelmessage',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channelmessage_receiver', to='backendApi.channel'),
        ),
        migrations.AlterField(
            model_name='channelmessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channelmessage_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='channelmuteduser',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channelmuteduser_channel', to='backendApi.channel'),
        ),
        migrations.AlterField(
            model_name='channelmuteduser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channelmuteduser_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gamescore',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamescore_game', to='backendApi.game'),
        ),
        migrations.AlterField(
            model_name='gamescore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamescore_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='muteduser',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='muteduser_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='muteduser',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='muteduser_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usermessage_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usermessage_sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
