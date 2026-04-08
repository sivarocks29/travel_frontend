"""Drivers admin URL configs."""
from django.urls import path
from .views import DriverListCreateView, DriverDetailView, AvailableDriversView, DriverLoginLogView, DriverAttendanceToggleView

urlpatterns = [
    path('drivers/', DriverListCreateView.as_view(), name='admin-driver-list'),
    path('drivers/<uuid:pk>/', DriverDetailView.as_view(), name='admin-driver-detail'),
    path('drivers/<uuid:pk>/attendance/', DriverAttendanceToggleView.as_view(), name='admin-driver-attendance'),
    path('drivers/available/', AvailableDriversView.as_view(), name='admin-driver-available'),
    path('driver-logs/', DriverLoginLogView.as_view(), name='admin-driver-logs'),
]
