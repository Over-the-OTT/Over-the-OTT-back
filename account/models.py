from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=20, unique=True)


class SubscribingOTT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ott = models.CharField(max_length=20)
    fee = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    share = models.IntegerField(null=True, blank=True)
