# Generated by Django 4.0.6 on 2023-03-04 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0010_skill_remove_customuser_skills_customuser_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Country',
            field=models.CharField(choices=[('USA', 'USA'), ('Canada', 'Canada')], default='USA', max_length=50),
        ),
    ]
