# Generated by Django 5.0.4 on 2024-04-26 08:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApi', '0009_alter_tournament_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='max_players',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='players',
            field=models.ManyToManyField(default=list, related_name='tournament_players', to=settings.AUTH_USER_MODEL),
        ),
    ]