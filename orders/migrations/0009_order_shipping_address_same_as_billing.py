# Generated by Django 3.2.4 on 2022-05-03 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20220408_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_address_same_as_billing',
            field=models.BooleanField(default=False),
        ),
    ]