"""
Vehicles app — Car/Vehicle Owner model.
Stores all vehicle documents and owner info.
"""
import uuid
from django.db import models
from accounts.models import User


def car_upload_path(instance, filename):
    return f'vehicles/{instance.vehicle_number}/{filename}'


class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='car_profile',
        limit_choices_to={'role': 'car'}
    )
    vehicle_id = models.CharField(max_length=20, unique=True, blank=True)
    vehicle_number = models.CharField(max_length=20, unique=True)
    owner_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)

    # Documents
    rc_document = models.FileField(upload_to=car_upload_path, blank=True, null=True)
    insurance_document = models.FileField(upload_to=car_upload_path, blank=True, null=True)
    permit_document = models.FileField(upload_to=car_upload_path, blank=True, null=True)
    aadhar_card = models.FileField(upload_to=car_upload_path, blank=True, null=True)
    license_document = models.FileField(upload_to=car_upload_path, blank=True, null=True)

    # Photos
    owner_photo = models.ImageField(upload_to=car_upload_path, blank=True, null=True)
    car_photo = models.ImageField(upload_to=car_upload_path, blank=True, null=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cars'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-generate vehicle_id like VEH-0001
        if not self.vehicle_id:
            last = Car.objects.order_by('-created_at').first()
            count = (Car.objects.count() + 1)
            self.vehicle_id = f'VEH-{count:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.vehicle_id} — {self.vehicle_number}'
