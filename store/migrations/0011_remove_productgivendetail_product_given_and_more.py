# Generated by Django 5.0 on 2024-02-09 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_product_productgiven_productgivendetail_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productgivendetail',
            name='product_given',
        ),
        migrations.RemoveField(
            model_name='productgivendetail',
            name='product',
        ),
        migrations.DeleteModel(
            name='ProductGiven',
        ),
        migrations.DeleteModel(
            name='ProductGivenDetail',
        ),
    ]
