# Generated by Django 3.2.13 on 2022-10-13 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_auto_20220712_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_path',
            field=models.ImageField(upload_to='', verbose_name='image_path'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, verbose_name='quantity'),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.BooleanField(default=True, verbose_name='status'),
        ),
    ]