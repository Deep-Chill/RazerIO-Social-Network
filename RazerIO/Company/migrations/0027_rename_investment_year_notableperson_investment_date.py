# Generated by Django 4.0.6 on 2023-03-16 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0026_notableperson_amount_invested_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notableperson',
            old_name='investment_year',
            new_name='investment_date',
        ),
    ]