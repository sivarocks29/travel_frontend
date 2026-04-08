"""Bookings admin URL configs."""
from django.urls import path
from .views import BookingListCreateView, BookingDetailView, PendingBookingsView, BookingAssignView

urlpatterns = [
    path('bookings/', BookingListCreateView.as_view(), name='admin-booking-list'),
    path('bookings/<uuid:pk>/', BookingDetailView.as_view(), name='admin-booking-detail'),
    path('bookings/pending/', PendingBookingsView.as_view(), name='admin-booking-pending'),
    path('bookings/<uuid:pk>/assign/', BookingAssignView.as_view(), name='admin-booking-assign'),
]
