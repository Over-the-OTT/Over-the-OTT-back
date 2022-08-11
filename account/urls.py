from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('addott/', SubscribingOTTView.as_view()),
    path('addott/<int:pk>/', SubsOTTDetailView.as_view()),
    path('ott/', OTTView.as_view()),
]
