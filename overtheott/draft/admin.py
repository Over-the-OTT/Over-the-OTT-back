from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'password']
    list_display_links = ['id', 'username']


@admin.register(OTT)
class OTTAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'fee']
    list_display_links = ['id', 'name']


@admin.register(SubscribingOTT)
class SubsOTTAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ott', 'start_date']
