# Generated by Django 5.0.3 on 2024-03-08 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_category_is_active_product_is_active_product_is_main_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_main',
            new_name='thumbnail',
        ),
    ]
