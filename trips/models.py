"""
Trips app — Trip/TripTask model auto-created when booking is made.
Tracks KM, photos, start/end times.
"""
import uuid
from django.db import models
from bookings.models import Booking
from vehicles.models import Car
from drivers.models import Driver


def trip_upload_path(instance, filename):
    return f'trips/{instance.booking.trip_no}/{filename}'


class Trip(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('started', 'Started'),
        ('completed', 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='trip')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='trips')
    vehicle = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='trips')

    # KM tracking
    start_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    end_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Photo upload by driver at trip start
    start_photo = models.ImageField(upload_to=trip_upload_path, null=True, blank=True)

    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'trips'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-calculate total KM
        if self.start_km is not None and self.end_km is not None:
            self.total_km = self.end_km - self.start_km
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Trip for {self.booking.trip_no}'
