# Generated by Django 4.0.6 on 2023-02-17 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='Shareprice',
            field=models.IntegerField(default=0),
        ),
    ]
