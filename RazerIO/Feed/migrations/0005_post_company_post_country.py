# Generated by Django 4.0.6 on 2023-03-18 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Country', '0001_initial'),
        ('Company', '0041_alter_notableperson_title'),
        ('Feed', '0004_alter_comment_date_commented_alter_upvote_date_voted'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Company.company'),
        ),
        migrations.AddField(
            model_name='post',
            name='Country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Country.country'),
        ),
    ]
