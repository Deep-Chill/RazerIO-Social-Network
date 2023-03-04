# Generated by Django 4.0.6 on 2023-03-03 23:44

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
            name='JobListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=100)),
                ('Job_Title', models.CharField(max_length=50)),
                ('Job_Description', models.TextField(max_length=5000)),
                ('Job_Requirements', models.TextField(max_length=5000)),
                ('salary_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_max', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Category', models.CharField(choices=[('Programming', 'Programming'), ('Administrative', 'Administrative'), ('Design', 'Design'), ('Sales & Marketing', 'Sales & Marketing')], max_length=50)),
                ('Job_Status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Filled', 'Filled')], max_length=10)),
                ('Location', models.CharField(choices=[('Sacramento', 'Sacramento'), ('San Diego', 'San Diego'), ('Los Angeles', 'Los Angeles'), ('Remote', 'Remote')], max_length=50)),
                ('Date_Posted', models.DateTimeField(auto_now_add=True)),
                ('Poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
