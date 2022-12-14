# Generated by Django 4.0.3 on 2022-05-12 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_remove_order_to_country_order_address_other_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100, verbose_name='client id')),
                ('customer_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='customer name')),
                ('customer_phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='customer phone')),
                ('customer_email', models.CharField(blank=True, max_length=100, null=True, verbose_name='customer email')),
                ('to_zip', models.CharField(blank=True, max_length=50, null=True, verbose_name='zip code')),
                ('to_city', models.CharField(blank=True, max_length=100, null=True, verbose_name='city')),
                ('to_street', models.CharField(blank=True, max_length=100, null=True, verbose_name='street')),
                ('to_house_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='house number')),
                ('address', models.TextField(blank=True, null=True, verbose_name='address')),
                ('customer_name_other', models.CharField(blank=True, max_length=100, null=True, verbose_name='other customer name')),
                ('customer_phone_other', models.CharField(blank=True, max_length=100, null=True, verbose_name='other customer phone')),
                ('customer_email_other', models.CharField(blank=True, max_length=100, null=True, verbose_name='other customer email')),
                ('to_zip_other', models.CharField(blank=True, max_length=50, null=True, verbose_name='other zip code')),
                ('to_city_other', models.CharField(blank=True, max_length=100, null=True, verbose_name='other city')),
                ('to_street_other', models.CharField(blank=True, max_length=100, null=True, verbose_name='other street')),
                ('to_house_number_other', models.CharField(blank=True, max_length=50, null=True, verbose_name='other house number')),
                ('address_other', models.TextField(blank=True, null=True, verbose_name='other address')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='address'),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='quantity')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='shop.CartProduct', to='shop.product'),
        ),
    ]
