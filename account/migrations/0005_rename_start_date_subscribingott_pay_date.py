# Generated by Django 4.0.4 on 2022-08-04 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_subscribingott_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscribingott',
            old_name='start_date',
            new_name='pay_date',
        ),
    ]
