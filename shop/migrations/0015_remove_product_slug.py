# Generated by Django 4.0.3 on 2022-05-06 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
