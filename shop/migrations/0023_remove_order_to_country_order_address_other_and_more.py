# Generated by Django 4.0.3 on 2022-05-12 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_alter_order_transaction_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='to_country',
        ),
        migrations.AddField(
            model_name='order',
            name='address_other',
            field=models.TextField(blank=True, null=True, verbose_name='other address'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_email_other',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='other customer email'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_name_other',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='other customer name'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_phone_other',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='other customer phone'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_city_other',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='other city'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_house_number',
            field=models.CharField(default='', max_length=50, verbose_name='house number'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_house_number_other',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='other house number'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_street_other',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='other street'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_zip_other',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='other zip code'),
        ),
    ]
