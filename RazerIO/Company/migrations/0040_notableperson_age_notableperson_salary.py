# Generated by Django 4.0.6 on 2023-03-18 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0039_remove_company_operatingmargin'),
    ]

    operations = [
        migrations.AddField(
            model_name='notableperson',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notableperson',
            name='salary',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
