# Generated by Django 4.0.6 on 2023-03-09 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0018_skill_user_skill_customuser_skill'),
        ('Projects', '0002_project_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='collaborator_requirements',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='location',
            field=models.CharField(blank=True, choices=[('Sacramento', 'Sacramento'), ('San Diego', 'San Diego'), ('Los Angeles', 'Los Angeles'), ('Remote', 'Remote')], max_length=50),
        ),
        migrations.AddField(
            model_name='project',
            name='looking_for_x_collaborators',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='required_skills',
            field=models.ManyToManyField(blank=True, related_name='required_for_collaborators', to='Users.skill'),
        ),
        migrations.AddField(
            model_name='project',
            name='tech_stack',
            field=models.ManyToManyField(blank=True, related_name='used_in_project', to='Users.skill'),
        ),
    ]
