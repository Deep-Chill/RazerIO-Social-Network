# Generated by Django 4.0.6 on 2023-03-15 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Users', '0032_remove_user_skill_projects'),
        ('Projects', '0009_rename_project_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='experience',
            old_name='collaborator_requirements',
            new_name='additional_info',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='required_skills',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='tech_stack',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='experience',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experience',
            name='item_type',
            field=models.CharField(choices=[('Project', 'Project'), ('Certification', 'Certification'), ('Publication', 'Publication'), ('Award', 'Award'), ('Volunteer Work', 'Volunteer Work'), ('Other', 'Other')], default='Project', max_length=15),
        ),
        migrations.AddField(
            model_name='experience',
            name='skills_used',
            field=models.ManyToManyField(blank=True, related_name='skills_used', to='Users.skill'),
        ),
        migrations.AddField(
            model_name='experience',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experience',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='collaborators',
            field=models.ManyToManyField(blank=True, related_name='collaborating_portfolio_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='experience',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_portfolio_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='experience',
            name='tools_used',
            field=models.ManyToManyField(blank=True, related_name='tools_used', to='Projects.tool'),
        ),
    ]
