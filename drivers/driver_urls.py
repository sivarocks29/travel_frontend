"""Driver panel URL configs."""
from django.urls import path
from .views import (
    DriverProfileView, DriverTasksView,
    TripStartView, TripEndView, DriverCommissionsView
)

urlpatterns = [
    path('profile/', DriverProfileView.as_view(), name='driver-profile'),
    path('tasks/', DriverTasksView.as_view(), name='driver-tasks'),
    path('tasks/<uuid:pk>/start/', TripStartView.as_view(), name='driver-trip-start'),
    path('tasks/<uuid:pk>/end/', TripEndView.as_view(), name='driver-trip-end'),
    path('commissions/', DriverCommissionsView.as_view(), name='driver-commissions'),
]
