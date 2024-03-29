# Generated by Django 4.0.6 on 2023-03-09 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0002_project_status'),
        ('Users', '0017_customuser_profilepic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User_Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience_years', models.IntegerField(default=0)),
                ('projects', models.ManyToManyField(to='Projects.project')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='Skill',
            field=models.ManyToManyField(through='Users.User_Skill', to='Users.skill'),
        ),
    ]
