# Generated by Django 4.0.6 on 2023-03-04 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0004_company_stockticker'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='Owners',
            new_name='Employees',
        ),
    ]
