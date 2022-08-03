from django.contrib import admin
from .models import *

@admin.register(TVContent)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'tmdb_id']
    list_display_links = ['id', 'title']

@admin.register(MovieContent)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'tmdb_id']
    list_display_links = ['id', 'title']

@admin.register(Episode)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'tv', 'episode_num']
    list_display_links = ['id', 'tv']