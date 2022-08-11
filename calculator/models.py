from django.db import models
from account.models import SubscribingOTT

# Create your models here.


class Runtime(models.Model):
    ott = models.ForeignKey(
        SubscribingOTT, on_delete=models.CASCADE, related_name='runtimes')
    year = models.IntegerField()
    month = models.IntegerField()
    total_runtime = models.IntegerField(default=0)

    @property
    def won_per_min(self):
        won_per_min = self.ott.ott.fee / self.total_runtime
        return won_per_min

    @property
    def ott_name(self):
        return self.ott.ott.ott

    def __str__(self):
        return f'{self.ott_name}'
