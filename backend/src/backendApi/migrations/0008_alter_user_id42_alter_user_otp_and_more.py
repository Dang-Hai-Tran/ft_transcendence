# Generated by Django 5.0.2 on 2024-02-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendApi', '0007_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id42',
            field=models.IntegerField(default=None, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp_expiration',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profilePicture',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
