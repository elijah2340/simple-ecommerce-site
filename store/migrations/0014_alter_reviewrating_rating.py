# Generated by Django 3.2.4 on 2022-05-03 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_reviewrating_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='rating',
            field=models.FloatField(blank=True),
        ),
    ]
