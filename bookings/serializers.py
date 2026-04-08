"""Bookings serializers."""
from rest_framework import serializers
from .models import Booking
from customers.serializers import CustomerAutoFillSerializer
from vehicles.serializers import CarListSerializer
from drivers.serializers import DriverListSerializer


class BookingSerializer(serializers.ModelSerializer):
    customer_detail = CustomerAutoFillSerializer(source='customer', read_only=True)
    vehicle_detail = CarListSerializer(source='vehicle', read_only=True)
    driver_detail = DriverListSerializer(source='driver', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'trip_no', 'booking_date',
            'pickup_date', 'pickup_time', 'drop_date', 'drop_time',
            'customer', 'customer_detail',
            'vehicle', 'vehicle_detail',
            'driver', 'driver_detail',
            'type_of_trip', 'pickup_location', 'drop_location',
            'fare', 'waiting_hours', 'is_new_customer',
            'status', 'rating', 'review',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'trip_no', 'booking_date', 'created_at', 'updated_at']

    def create(self, validated_data):
        from trips.models import Trip
        from commissions.models import Commission, CommissionDefault
        booking = Booking.objects.create(**validated_data)

        # Auto-create Trip task
        trip = Trip.objects.create(
            booking=booking,
            driver=booking.driver,
            vehicle=booking.vehicle,
        )

        # Auto-create Commission with default split
        defaults = CommissionDefault.objects.first()
        if defaults:
            car_pct = defaults.car_percentage
            driver_pct = defaults.driver_percentage
            admin_pct = defaults.admin_percentage
        else:
            car_pct, driver_pct, admin_pct = 60, 30, 10

        Commission.objects.create(
            booking=booking,
            total_amount=booking.fare,
            car_percentage=car_pct,
            driver_percentage=driver_pct,
            admin_percentage=admin_pct,
        )

        return booking


class BookingAssignSerializer(serializers.ModelSerializer):
    """Used only for assigning/updating driver + car on a booking."""
    class Meta:
        model = Booking
        fields = ['vehicle', 'driver', 'status']

    def update(self, instance, validated_data):
        from trips.models import Trip
        instance.vehicle = validated_data.get('vehicle', instance.vehicle)
        instance.driver = validated_data.get('driver', instance.driver)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Sync the trip task
        if hasattr(instance, 'trip'):
            instance.trip.driver = instance.driver
            instance.trip.vehicle = instance.vehicle
            instance.trip.save()

        return instance
