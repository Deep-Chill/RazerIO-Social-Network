# Generated by Django 4.0.6 on 2023-03-13 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0028_remove_customuser_company_verified_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Company_Verified_Email',
            field=models.BooleanField(default=False),
        ),
    ]