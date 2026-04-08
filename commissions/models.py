"""
Commissions app — Commission model per booking.
Stores percentage splits and auto-calculates amounts.
"""
import uuid
from django.db import models
from bookings.models import Booking


class Commission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='commission')

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Percentage splits (set by admin per booking or globally)
    car_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=60)
    driver_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    admin_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)

    # Calculated amounts (auto-filled on save)
    car_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    driver_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admin_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'commissions'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-calculate commission amounts from percentages
        if self.total_amount:
            self.car_amount = (self.total_amount * self.car_percentage) / 100
            self.driver_amount = (self.total_amount * self.driver_percentage) / 100
            self.admin_amount = (self.total_amount * self.admin_percentage) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Commission for {self.booking.trip_no} — Total: {self.total_amount}'


class CommissionDefault(models.Model):
    """Global default commission split. Admin can update this."""
    car_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=60)
    driver_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    admin_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'commission_defaults'

    def __str__(self):
        return f'Default: Car={self.car_percentage}% Driver={self.driver_percentage}% Admin={self.admin_percentage}%'
