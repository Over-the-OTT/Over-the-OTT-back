# Generated by Django 4.0.6 on 2022-08-15 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribingott',
            name='ott',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.ott'),
        ),
    ]
