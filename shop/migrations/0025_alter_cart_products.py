# Generated by Django 4.0.3 on 2022-05-12 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_cart_alter_order_address_cartproduct_cart_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, through='shop.CartProduct', to='shop.product'),
        ),
    ]
