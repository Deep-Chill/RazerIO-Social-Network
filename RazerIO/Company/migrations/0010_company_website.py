# Generated by Django 4.0.6 on 2023-03-11 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0009_remove_company_is_university_alter_company_about_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='Website',
            field=models.URLField(blank=True),
        ),
    ]
