from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import datetime
from dateutil import relativedelta

OTT_CHOICE = (
    ('Netflix', 'Netflix'),
    ('Watcha', 'Watcha'),
    ('Disney Plus', 'Disney Plus'),
    ('wavve', 'Wavve'),
    ('Amazon Prime Video', 'Amazon Prime Video'),
    ('Apple TV Plus', 'Apple TV Plus')
)

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email=self.normalize_email(email), password=password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(max_length=20, unique=True)
    username = models.CharField(max_length=40, unique=False, default='')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class OTT(models.Model):
    ott = models.CharField(max_length=20, choices=OTT_CHOICE)
    membership = models.CharField(max_length=30)
    fee = models.IntegerField()

    def __str__(self):
        return f'{self.ott} ({self.membership})'


class SubscribingOTT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ott = models.ForeignKey(OTT, on_delete=models.CASCADE, null=True)
    pay_date = models.SmallIntegerField(null=True, blank=True)
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

    @property
    def pay_amount(self):
        return self.ott.fee/self.share

    def __str__(self):
        return f'{self.ott.ott} ({self.user})'
