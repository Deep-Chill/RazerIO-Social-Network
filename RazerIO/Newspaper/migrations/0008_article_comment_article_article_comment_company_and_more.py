# Generated by Django 4.0.6 on 2023-03-05 00:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Company', '0005_rename_owners_company_employees'),
        ('Newspaper', '0007_alter_article_date_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='article_comment',
            name='Article',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Newspaper.article'),
        ),
        migrations.AddField(
            model_name='article_comment',
            name='Company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Company.company'),
        ),
        migrations.AddField(
            model_name='article_comment',
            name='Is_Anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article_comment',
            name='Show_Company',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='article_comment',
            name='Author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article_comment',
            name='Date_Published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]