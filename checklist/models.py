import re
from django.db import models
from account.models import User

OTT_CHOICE = (
    ('Netflix', 'Netflix'),
    ('Watcha', 'Watcha'),
    ('Disney Plus', 'Disney Plus'),
    ('Wavve', 'Wavve'),
    ('Prime Video', 'Prime Video'),
    ('Apple TV', 'Apple TV')
)


class TVContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    tmdb_id = models.TextField()
    poster = models.TextField()
    provider = models.CharField(max_length=20, choices=OTT_CHOICE)
    season = models.IntegerField()
    total_episode = models.IntegerField()
    episode_status = models.IntegerField(default=0)
    runtime = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Episode(models.Model):
    tv = models.ForeignKey(
        TVContent, related_name='episodes', on_delete=models.CASCADE)
    episode_num = models.IntegerField()
    is_finished = models.BooleanField(default=False)


class MovieContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    tmdb_id = models.TextField()
    poster = models.TextField()
    provider = models.CharField(max_length=20, choices=OTT_CHOICE)
    runtime = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
