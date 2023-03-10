# Generated by Django 4.0.6 on 2023-03-10 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Company', '0006_company_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='LastEditedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edited_companies', to=settings.AUTH_USER_MODEL),
        ),
    ]
