# Generated by Django 4.0.6 on 2023-03-07 21:25

import Users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0016_remove_customuser_skills_delete_skill'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='ProfilePic',
            field=models.ImageField(blank=True, null=True, upload_to=Users.models.upload_to),
        ),
    ]
