# Generated by Django 4.0.6 on 2023-03-12 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0011_company_is_university'),
        ('Users', '0021_remove_education_institution_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='institution',
            field=models.ForeignKey(blank=True, default=None, limit_choices_to={'Is_University': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='Company.company'),
        ),
    ]