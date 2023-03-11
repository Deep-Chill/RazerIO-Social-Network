# Generated by Django 4.0.6 on 2023-03-11 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0011_company_is_university'),
        ('Users', '0020_alter_education_degree_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='institution_name',
        ),
        migrations.AddField(
            model_name='education',
            name='institution',
            field=models.ForeignKey(blank=True, default=None, limit_choices_to={'Is_Institution': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='Company.company'),
        ),
    ]
