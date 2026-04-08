"""Trips views — Admin list view."""
from rest_framework import generics
from .models import Trip
from .serializers import TripSerializer
from accounts.permissions import IsAdmin


class TripListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = TripSerializer
    queryset = Trip.objects.select_related('booking', 'driver', 'vehicle').all()
    filterset_fields = ['status', 'driver', 'vehicle']
    search_fields = ['booking__trip_no']
