# Generated by Django 4.2.3 on 2023-07-31 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_bep20_address_order_purpose_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.BooleanField(default=False),
        ),
    ]