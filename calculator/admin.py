from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Runtime)
class RuntimeAdmin(admin.ModelAdmin):
    list_display = ['ott', 'year', 'month', 'total_runtime']
    list_display_links = ['ott', 'total_runtime']
