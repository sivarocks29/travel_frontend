"""Drivers views — Admin CRUD + Driver Panel views."""
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Driver, DriverLoginLog
from .serializers import DriverSerializer, DriverListSerializer, DriverLoginLogSerializer
from accounts.permissions import IsAdmin, IsDriver
from trips.models import Trip
from trips.serializers import TripSerializer, TripStartSerializer, TripEndSerializer
from commissions.models import Commission
from commissions.serializers import CommissionSerializer


# ──── Admin ────────────────────────────────────────────────────────────────
class DriverListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DriverSerializer
    queryset = Driver.objects.select_related('user').all()
    filterset_fields = ['is_logged_in']
    search_fields = ['user__username', 'license_number', 'mobile_number']


class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class DriverAttendanceToggleView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            driver = Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:
            return Response({'error': 'Driver not found'}, status=404)
        
        is_logged_in = request.data.get('is_logged_in', False)
        
        if is_logged_in and not driver.is_logged_in:
            driver.is_logged_in = True
            driver.last_login_at = timezone.now()
            DriverLoginLog.objects.create(driver=driver, login_at=driver.last_login_at)
        elif not is_logged_in and driver.is_logged_in:
            driver.is_logged_in = False
            driver.last_logout_at = timezone.now()
            log = DriverLoginLog.objects.filter(driver=driver, logout_at__isnull=True).last()
            if log:
                log.logout_at = driver.last_logout_at
                log.save()
        
        driver.save()
        return Response(DriverSerializer(driver).data)



class AvailableDriversView(generics.ListAPIView):
    """Drivers currently logged in — shown during booking allocation."""
    permission_classes = [IsAdmin]
    serializer_class = DriverListSerializer
    queryset = Driver.objects.filter(is_logged_in=True)


class DriverLoginLogView(generics.ListAPIView):
    """Admin: view login/logout history of a driver (filter by driver_id)."""
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = DriverLoginLog.objects.select_related('driver__user').all()
        driver_id = self.request.query_params.get('driver_id')
        if driver_id:
            qs = qs.filter(driver_id=driver_id)
        return qs

    def get_serializer_class(self):
        from rest_framework import serializers as drf_serializers

        class DriverLogSerializer(DriverLoginLogSerializer):
            driver_name = drf_serializers.CharField(source='driver.name', read_only=True)
            driver_username = drf_serializers.CharField(source='driver.user.username', read_only=True)
            driver_id = drf_serializers.UUIDField(source='driver.id', read_only=True)

            class Meta(DriverLoginLogSerializer.Meta):
                fields = ['id', 'driver_id', 'driver_name', 'driver_username', 'login_at', 'logout_at', 'created_at']

        return DriverLogSerializer


# ──── Driver Panel ──────────────────────────────────────────────────────────
class DriverProfileView(APIView):
    permission_classes = [IsDriver]

    def get(self, request):
        driver = request.user.driver_profile
        return Response(DriverSerializer(driver).data)


class DriverTasksView(generics.ListAPIView):
    permission_classes = [IsDriver]
    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.filter(driver=self.request.user.driver_profile).select_related('booking')


class TripStartView(APIView):
    permission_classes = [IsDriver]

    def patch(self, request, pk):
        try:
            trip = Trip.objects.get(pk=pk, driver=request.user.driver_profile)
        except Trip.DoesNotExist:
            return Response({'error': 'Trip not found'}, status=404)
        serializer = TripStartSerializer(data=request.data)
        if serializer.is_valid():
            trip.start_km = serializer.validated_data['start_km']
            trip.start_photo = serializer.validated_data.get('start_photo')
            trip.status = 'started'
            trip.started_at = timezone.now()
            trip.booking.status = 'ongoing'
            trip.booking.save()
            trip.save()
            return Response(TripSerializer(trip).data)
        return Response(serializer.errors, status=400)


class TripEndView(APIView):
    permission_classes = [IsDriver]

    def patch(self, request, pk):
        try:
            trip = Trip.objects.get(pk=pk, driver=request.user.driver_profile)
        except Trip.DoesNotExist:
            return Response({'error': 'Trip not found'}, status=404)
        serializer = TripEndSerializer(data=request.data)
        if serializer.is_valid():
            trip.end_km = serializer.validated_data['end_km']
            trip.status = 'completed'
            trip.ended_at = timezone.now()
            trip.booking.status = 'completed'
            trip.booking.save()
            trip.save()
            return Response(TripSerializer(trip).data)
        return Response(serializer.errors, status=400)


class DriverCommissionsView(generics.ListAPIView):
    permission_classes = [IsDriver]
    serializer_class = CommissionSerializer

    def get_queryset(self):
        driver = self.request.user.driver_profile
        return Commission.objects.filter(booking__driver=driver)
