# Generated by Django 4.0.6 on 2022-08-09 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ott', models.CharField(choices=[('Netflix', 'Netflix'), ('Watcha', 'Watcha'), ('Disney Plus', 'Disney Plus'), ('Wavve', 'Wavve'), ('Prime Video', 'Prime Video'), ('Apple TV', 'Apple TV')], max_length=20)),
                ('membership', models.CharField(max_length=30)),
                ('fee', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='subscribingott',
            name='fee',
        ),
        migrations.AlterField(
            model_name='subscribingott',
            name='ott',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.ott'),
        ),
    ]