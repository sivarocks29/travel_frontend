"""Vehicles car-panel URL configs."""
from django.urls import path
from .views import CarProfileView, CarTripsView, CarTripsKmUpdateView, CarCommissionsView

urlpatterns = [
    path('profile/', CarProfileView.as_view(), name='car-profile'),
    path('trips/', CarTripsView.as_view(), name='car-trips'),
    path('trips/<uuid:pk>/km/', CarTripsKmUpdateView.as_view(), name='car-trip-km'),
    path('commissions/', CarCommissionsView.as_view(), name='car-commissions'),
]
