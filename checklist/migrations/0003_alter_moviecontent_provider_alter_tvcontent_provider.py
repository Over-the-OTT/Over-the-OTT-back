# Generated by Django 4.0.6 on 2022-08-18 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0002_alter_moviecontent_provider_alter_tvcontent_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviecontent',
            name='provider',
            field=models.CharField(choices=[('Netflix', 'Netflix'), ('Watcha', 'Watcha'), ('Disney Plus', 'Disney Plus'), ('wavve', 'wavve'), ('Amazon Prime Video', 'Amazon Prime Video'), ('Apple TV Plus', 'Apple TV Plus')], max_length=20),
        ),
        migrations.AlterField(
            model_name='tvcontent',
            name='provider',
            field=models.CharField(choices=[('Netflix', 'Netflix'), ('Watcha', 'Watcha'), ('Disney Plus', 'Disney Plus'), ('wavve', 'wavve'), ('Amazon Prime Video', 'Amazon Prime Video'), ('Apple TV Plus', 'Apple TV Plus')], max_length=20),
        ),
    ]
