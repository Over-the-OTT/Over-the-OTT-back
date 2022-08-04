from django.db import models
from account.models import User, SubscribingOTT
# Create your models here.


class Runtime(models.Model):
    ott = models.ForeignKey(SubscribingOTT, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total_runtime = models.IntegerField()

    @property
    def won_per_min(self):
        won_per_min = self.ott.fee / self.total_runtime
        return won_per_min

    @property
    def ott_name(self):
        return self.ott.ott
