# Generated by Django 4.0.6 on 2023-03-04 01:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Newspaper', '0005_rename_article_comments_article_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
