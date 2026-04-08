"""Trips serializers."""
from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    trip_no = serializers.CharField(source='booking.trip_no', read_only=True)
    customer_name = serializers.CharField(source='booking.customer.name', read_only=True)
    pickup_location = serializers.CharField(source='booking.pickup_location', read_only=True)
    drop_location = serializers.CharField(source='booking.drop_location', read_only=True)
    pickup_date = serializers.DateField(source='booking.pickup_date', read_only=True)
    fare = serializers.DecimalField(source='booking.fare', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'trip_no', 'customer_name',
            'pickup_location', 'drop_location', 'pickup_date', 'fare',
            'start_km', 'end_km', 'total_km',
            'start_photo', 'started_at', 'ended_at', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_km', 'created_at', 'updated_at']


class TripStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['start_km', 'start_photo']


class TripEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['end_km']
