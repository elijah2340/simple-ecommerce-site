# Generated by Django 3.2.4 on 2022-05-01 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220408_1157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='is_superadmin',
            new_name='is_superuser',
        ),
    ]
