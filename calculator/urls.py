from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'calculator'

urlpatterns = [
    path('runtime/', RuntimeView.as_view()),
]
