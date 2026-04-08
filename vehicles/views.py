"""Vehicles views — Admin CRUD + Car Panel views."""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Car
from .serializers import CarSerializer, CarListSerializer
from accounts.permissions import IsAdmin, IsCarOwner
from trips.models import Trip
from trips.serializers import TripSerializer
from commissions.models import Commission
from commissions.serializers import CommissionSerializer


# ──── Admin ────────────────────────────────────────────────────────────────
class CarListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CarSerializer
    queryset = Car.objects.select_related('user').all()
    filterset_fields = ['is_available']
    search_fields = ['vehicle_number', 'owner_name', 'vehicle_id']


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class CarDropdownView(generics.ListAPIView):
    """Available cars for booking dropdown."""
    permission_classes = [IsAdmin]
    serializer_class = CarListSerializer
    queryset = Car.objects.filter(is_available=True)


# ──── Car Panel ─────────────────────────────────────────────────────────────
class CarProfileView(APIView):
    permission_classes = [IsCarOwner]

    def get(self, request):
        car = request.user.car_profile
        return Response(CarSerializer(car).data)


class CarTripsView(generics.ListAPIView):
    permission_classes = [IsCarOwner]
    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.filter(vehicle=self.request.user.car_profile).select_related('booking')


class CarTripsKmUpdateView(generics.UpdateAPIView):
    permission_classes = [IsCarOwner]
    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.filter(vehicle=self.request.user.car_profile)

    def patch(self, request, *args, **kwargs):
        trip = self.get_object()
        trip.start_km = request.data.get('start_km', trip.start_km)
        trip.end_km = request.data.get('end_km', trip.end_km)
        trip.save()
        return Response(TripSerializer(trip).data)


class CarCommissionsView(generics.ListAPIView):
    permission_classes = [IsCarOwner]
    serializer_class = CommissionSerializer

    def get_queryset(self):
        car = self.request.user.car_profile
        return Commission.objects.filter(booking__vehicle=car)
