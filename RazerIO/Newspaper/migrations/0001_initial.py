# Generated by Django 4.0.6 on 2023-02-17 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Newspaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_Created', models.DateField(auto_created=True)),
                ('Title', models.CharField(max_length=256)),
                ('Owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Newspaper', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]