"""Customers serializers."""
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'customer_id', 'name', 'mobile_number',
            'email', 'address', 'total_bookings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'customer_id', 'total_bookings', 'created_at', 'updated_at']


class CustomerAutoFillSerializer(serializers.ModelSerializer):
    """Used for auto-fill in booking form."""
    class Meta:
        model = Customer
        fields = ['id', 'customer_id', 'name', 'mobile_number', 'email', 'address']
