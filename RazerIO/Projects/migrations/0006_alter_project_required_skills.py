# Generated by Django 4.0.6 on 2023-03-10 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0018_skill_user_skill_customuser_skill'),
        ('Projects', '0005_project_benefits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='required_skills',
            field=models.ManyToManyField(blank=True, max_length=3, related_name='required_for_collaborators', to='Users.skill'),
        ),
    ]