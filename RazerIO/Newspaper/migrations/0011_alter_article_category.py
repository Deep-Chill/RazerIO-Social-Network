# Generated by Django 4.0.6 on 2023-03-14 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Newspaper', '0010_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Category',
            field=models.CharField(blank=True, choices=[('Technology & Programming', 'Technology & Programming'), ('Artificial Intelligence', 'Artificial Intelligence'), ('Business & Industry', 'Business & Industry'), ('Opinion & Analysis', 'Opinion & Analysis'), ('General', 'General')], max_length=50),
        ),
    ]
