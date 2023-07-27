# Generated by Django 4.0.6 on 2023-03-17 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0034_alter_company_marketcap_alter_company_stockprice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='MarketCap',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='StockPrice',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=15, null=True),
        ),
    ]