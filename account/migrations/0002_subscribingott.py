# Generated by Django 4.0.4 on 2022-07-31 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribingOTT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ott', models.CharField(max_length=20)),
                ('fee', models.IntegerField(blank=True)),
                ('start_date', models.DateField(blank=True)),
                ('share', models.IntegerField(blank=True)),
            ],
        ),
    ]