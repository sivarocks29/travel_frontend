"""
Bookings app — Core booking model.
Supports partial allocation (car/driver can be null initially).
"""
import uuid
from django.db import models
from customers.models import Customer
from vehicles.models import Car
from drivers.models import Driver
from accounts.models import User


class Booking(models.Model):
    TRIP_TYPE_CHOICES = [
        ('local', 'Local'),
        ('outstation', 'Outstation'),
        ('airport', 'Airport'),
        ('rental', 'Rental'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip_no = models.CharField(max_length=20, unique=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    # Schedule
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    drop_date = models.DateField(null=True, blank=True)
    drop_time = models.TimeField(null=True, blank=True)

    # Parties (vehicle and driver can be unassigned initially)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='bookings')
    vehicle = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_bookings')

    # Trip details
    type_of_trip = models.CharField(max_length=20, choices=TRIP_TYPE_CHOICES, default='local')
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255, blank=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    waiting_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_new_customer = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Feedback
    rating = models.IntegerField(null=True, blank=True)
    review = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-generate trip_no like TRIP-00001
        if not self.trip_no:
            count = Booking.objects.count() + 1
            self.trip_no = f'TRIP-{count:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.trip_no} — {self.customer.name}'
