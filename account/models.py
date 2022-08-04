from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from dateutil import relativedelta

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=20, unique=True)


class SubscribingOTT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ott = models.CharField(max_length=20)
    fee = models.IntegerField(null=True, blank=True)
    pay_date = models.IntegerField(null=True, blank=True)
    share = models.IntegerField(null=True, blank=True)

    @property
    def next_pay(self):
        currentYear = datetime.datetime.now().year
        currentMonth = datetime.datetime.now().month
        currentDay = datetime.datetime.now().day
        if datetime.date(currentYear, currentMonth, currentDay) <= datetime.date(currentYear, currentMonth, self.pay_date):
            next_pay = datetime.date(
                currentYear, currentMonth, self.pay_date)
        else:
            next_pay = datetime.date(
                currentYear, currentMonth, self.pay_date) + relativedelta.relativedelta(months=1)
        return next_pay

    @property
    def days_till_pay(self):
        days_till = self.next_pay - datetime.date.today()
        return days_till.days
