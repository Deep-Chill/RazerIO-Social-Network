# Generated by Django 4.0.6 on 2023-03-18 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0040_notableperson_age_notableperson_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notableperson',
            name='title',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
