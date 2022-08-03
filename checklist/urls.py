from django.urls import path
from .views import MovieSearchView, TVSearchView, MovieListView, MovieDetailView, TVListView, TVDetailView

app_name = 'checklist'

urlpatterns = [
    path('search/movie/', MovieSearchView.as_view()),
    path('search/tv/', TVSearchView.as_view()),
    path('tv/', TVListView.as_view()),
    path('tv/<int:pk>/', TVDetailView.as_view()),
    path('movie/', MovieListView.as_view()),
    path('movie/<int:pk>/', MovieDetailView.as_view()),
]