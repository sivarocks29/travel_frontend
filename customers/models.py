"""
Customers app — Customer model with unique auto-generated Customer ID.
Supports auto-fill during booking creation.
"""
import uuid
from django.db import models


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    total_bookings = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-generate customer_id like CUST-0001
        if not self.customer_id:
            count = Customer.objects.count() + 1
            self.customer_id = f'CUST-{count:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer_id} — {self.name}'
