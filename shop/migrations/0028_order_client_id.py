# Generated by Django 3.2.13 on 2022-06-19 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_alter_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client_id',
            field=models.CharField(default='', max_length=100, verbose_name='client id'),
            preserve_default=False,
        ),
    ]
