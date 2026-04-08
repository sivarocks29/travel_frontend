"""Vehicles serializers."""
from rest_framework import serializers
from .models import Car
from accounts.serializers import UserSerializer, CreateUserSerializer


class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Car
        fields = [
            'id', 'user', 'username', 'password',
            'vehicle_id', 'vehicle_number', 'owner_name', 'mobile_number',
            'rc_document', 'insurance_document', 'permit_document',
            'aadhar_card', 'license_document', 'owner_photo', 'car_photo',
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'vehicle_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        from accounts.models import User
        username = validated_data.pop('username')
        password = validated_data.pop('password', 'changeme123')
        user = User.objects.create_user(username=username, password=password, role='car')
        car = Car.objects.create(user=user, **validated_data)
        return car


class CarListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for dropdown lists."""
    class Meta:
        model = Car
        fields = ['id', 'vehicle_id', 'vehicle_number', 'owner_name', 'is_available']
