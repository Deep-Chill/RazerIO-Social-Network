# Generated by Django 4.0.6 on 2023-03-15 03:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0032_remove_user_skill_projects'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Projects', '0008_alter_project_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Project',
            new_name='Experience',
        ),
    ]
