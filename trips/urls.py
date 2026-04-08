"""Trips admin URL configs."""
from django.urls import path
from .views import TripListView

urlpatterns = [
    path('trips/', TripListView.as_view(), name='admin-trips'),
]
