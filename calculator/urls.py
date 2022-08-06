from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'calculator'

urlpatterns = [
    path('runtime/', RuntimeView.as_view()),
<<<<<<< HEAD
    path('days-till/', DaysTillView.as_view()),
]
=======
    path('days_till/', DaysTillView.as_view()),

>>>>>>> 0df844630dcf35fa8f188d33f6bb8c5a94be2e3e
