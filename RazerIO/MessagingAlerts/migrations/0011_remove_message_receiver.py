# Generated by Django 4.0.6 on 2023-03-08 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MessagingAlerts', '0010_alter_alert_actor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
    ]