from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'password']
    list_display_links = ['id', 'username']


@admin.register(SubscribingOTT)
class OTTAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ott', 'fee', 'pay_date', 'share']
    list_display_linkes = ['id', 'ott']
