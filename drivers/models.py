"""
Drivers app — Driver model with login tracking.
Tracks login/logout timestamps to show availability during booking.
"""
import uuid
from django.db import models
from accounts.models import User


def driver_upload_path(instance, filename):
    return f'drivers/{instance.license_number}/{filename}'


class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='driver_profile',
        limit_choices_to={'role': 'driver'}
    )
    license_number = models.CharField(max_length=30, unique=True)
    photo = models.ImageField(upload_to=driver_upload_path, blank=True, null=True)
    aadhar_card = models.FileField(upload_to=driver_upload_path, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    # Login tracking
    is_logged_in = models.BooleanField(default=False)
    last_login_at = models.DateTimeField(null=True, blank=True)
    last_logout_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drivers'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.license_number}'


class DriverLoginLog(models.Model):
    """Records every login and logout event for a driver."""
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='login_logs')
    login_at = models.DateTimeField(null=True, blank=True)
    logout_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'driver_login_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.driver} — {self.login_at}'
