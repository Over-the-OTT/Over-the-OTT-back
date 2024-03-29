# Generated by Django 4.0.4 on 2022-08-11 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TVContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('tmdb_id', models.TextField()),
                ('poster', models.TextField()),
                ('provider', models.CharField(choices=[('Netflix', 'Netflix'), ('Watcha', 'Watcha'), ('Disney Plus', 'Disney Plus'), ('Wavve', 'Wavve'), ('Prime Video', 'Prime Video'), ('Apple TV', 'Apple TV')], max_length=20)),
                ('season', models.IntegerField()),
                ('total_episode', models.IntegerField()),
                ('episode_status', models.IntegerField(default=0)),
                ('runtime', models.IntegerField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MovieContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('tmdb_id', models.TextField()),
                ('poster', models.TextField()),
                ('provider', models.CharField(choices=[('Netflix', 'Netflix'), ('Watcha', 'Watcha'), ('Disney Plus', 'Disney Plus'), ('Wavve', 'Wavve'), ('Prime Video', 'Prime Video'), ('Apple TV', 'Apple TV')], max_length=20)),
                ('runtime', models.IntegerField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode_num', models.IntegerField()),
                ('is_finished', models.BooleanField(default=False)),
                ('tv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='checklist.tvcontent')),
            ],
        ),
    ]
