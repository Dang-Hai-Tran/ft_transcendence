# Generated by Django 5.0.4 on 2024-04-26 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApi', '0008_remove_game_loser_remove_game_loserscore_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='status',
            field=models.CharField(choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], default='upcoming', max_length=20),
        ),
    ]