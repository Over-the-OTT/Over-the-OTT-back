from rest_framework import serializers
from account.models import *
from .models import *


class RuntimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Runtime
        fields = ['ott_name', 'year', 'month', 'total_runtime', 'won_per_min']


class DaysTillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribingOTT
        fields = ['ott', 'next_pay', 'days_till_pay']
