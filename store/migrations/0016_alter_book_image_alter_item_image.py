# Generated by Django 5.0.2 on 2024-02-26 09:39

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_remove_book_category_remove_item_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='andelus/store/book/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='andelus/store/item/'),
        ),
    ]
