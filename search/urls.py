#search/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_flights_view, name='search_flights'),  # Use the correct view function
]
