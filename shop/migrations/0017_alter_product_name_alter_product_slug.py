# Generated by Django 4.0.3 on 2022-05-06 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='slug'),
        ),
    ]
