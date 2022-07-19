from django.urls import path
from .views import *

app_name = 'draft'

urlpatterns = [
    path('ott/', OTTView.as_view()),
    path('subsott/', SubsOTTView.as_view()),
    path('towatch/', ToWatchView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
]
