# Generated by Django 3.2.15 on 2022-11-17 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_interested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]