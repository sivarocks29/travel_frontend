"""Vehicles URL configs for admin prefix."""
from django.urls import path
from .views import CarListCreateView, CarDetailView, CarDropdownView

urlpatterns = [
    path('vehicles/', CarListCreateView.as_view(), name='admin-vehicle-list'),
    path('vehicles/<uuid:pk>/', CarDetailView.as_view(), name='admin-vehicle-detail'),
    path('vehicles/dropdown/', CarDropdownView.as_view(), name='admin-vehicle-dropdown'),
]
