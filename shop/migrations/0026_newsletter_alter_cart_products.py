# Generated by Django 4.0.3 on 2022-05-25 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_alter_cart_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_email', models.CharField(max_length=100, verbose_name='customer email')),
            ],
        ),
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='shop.CartProduct', to='shop.product'),
        ),
    ]