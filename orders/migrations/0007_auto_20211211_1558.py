# Generated by Django 3.2.4 on 2021-12-11 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_variation_managers'),
        ('orders', '0006_alter_orderproduct_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]
