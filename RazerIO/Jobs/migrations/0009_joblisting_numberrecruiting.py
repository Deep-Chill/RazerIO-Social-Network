# Generated by Django 4.0.6 on 2023-03-10 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Jobs', '0008_joblisting_applicationurl_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='joblisting',
            name='NumberRecruiting',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
