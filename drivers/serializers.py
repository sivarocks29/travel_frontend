"""Drivers serializers."""
from rest_framework import serializers
from .models import Driver, DriverLoginLog
from accounts.serializers import UserSerializer


class DriverLoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLoginLog
        fields = ['id', 'login_at', 'logout_at', 'created_at']


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # username and password are optional — auto-generated if absent
    username = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    login_logs = DriverLoginLogSerializer(many=True, read_only=True)

    class Meta:
        model = Driver
        fields = [
            'id', 'user', 'username', 'password',
            'name', 'age',
            'license_number', 'photo', 'aadhar_card',
            'mobile_number', 'address',
            'is_logged_in', 'last_login_at', 'last_logout_at',
            'login_logs', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_logged_in', 'last_login_at', 'last_logout_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        from accounts.models import User
        license_number = validated_data.get('license_number', '')
        # Auto-generate username from license number if not provided
        username = validated_data.pop('username', '').strip() or f"driver_{license_number.lower().replace(' ', '_')}"
        password = validated_data.pop('password', '').strip() or 'changeme123'
        user = User.objects.create_user(username=username, password=password, role='driver')
        driver = Driver.objects.create(user=user, **validated_data)
        return driver


class DriverListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for available driver dropdown."""
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Driver
        fields = ['id', 'username', 'name', 'age', 'license_number', 'mobile_number', 'is_logged_in', 'last_login_at', 'last_logout_at']
