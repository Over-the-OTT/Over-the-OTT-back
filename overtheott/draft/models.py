from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=20, unique=True)


class OTT(models.Model):
    name = models.CharField(max_length=10, unique=True)
    fee = models.IntegerField(null=True, default=0)


class SubscribingOTT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ott = models.ForeignKey(
        OTT, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)


# 모델 하나에 booleanField를 넣어서 프런트에서 거름? 모델을 따로 만들어서 데이터를 이동함?
class ToWatchContent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='towatch')
    content_id = models.IntegerField()
    ott = models.ForeignKey(
        SubscribingOTT, on_delete=models.CASCADE, null=True, default="")
    added_at = models.DateTimeField(auto_now_add=True)


class WatchedContent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watched')
    content_id = models.IntegerField()
    ott = models.ForeignKey(
        SubscribingOTT, on_delete=models.CASCADE, null=True, default="")
    added_at = models.DateTimeField(auto_now_add=True)
