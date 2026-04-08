"""Commissions serializers."""
from rest_framework import serializers
from .models import Commission, CommissionDefault


class CommissionSerializer(serializers.ModelSerializer):
    trip_no = serializers.CharField(source='booking.trip_no', read_only=True)
    customer_name = serializers.CharField(source='booking.customer.name', read_only=True)

    class Meta:
        model = Commission
        fields = [
            'id', 'trip_no', 'customer_name',
            'total_amount',
            'car_percentage', 'driver_percentage', 'admin_percentage',
            'car_amount', 'driver_amount', 'admin_amount',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'car_amount', 'driver_amount', 'admin_amount', 'created_at', 'updated_at']


class CommissionDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionDefault
        fields = ['id', 'car_percentage', 'driver_percentage', 'admin_percentage', 'updated_at']
        read_only_fields = ['id', 'updated_at']
