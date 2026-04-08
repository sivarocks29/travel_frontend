"""
Seed script for Pyolliv Fleet Management System.
Creates default admin user, commission defaults, and sample data.

Usage:
    cd pyolliv_backend
    source venv/bin/activate
    python manage.py shell < seed.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyolliv.settings')

# -- Admin user
from accounts.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(username='admin', password='admin123', email='admin@pyolliv.com')
    print('✅ Admin user created: admin / admin123')
else:
    print('ℹ️  Admin user already exists')

# -- Commission defaults
from commissions.models import CommissionDefault
defaults, created = CommissionDefault.objects.get_or_create(pk=1, defaults={
    'car_percentage': 60,
    'driver_percentage': 30,
    'admin_percentage': 10,
})
if created:
    print('✅ Commission defaults created: Car=60%, Driver=30%, Admin=10%')
else:
    print('ℹ️  Commission defaults already exist')

# -- Sample car owner
if not User.objects.filter(username='car_owner_1').exists():
    from vehicles.models import Car
    car_user = User.objects.create_user(username='car_owner_1', password='car123', role='car')
    Car.objects.create(
        user=car_user,
        vehicle_number='TN01AB1234',
        owner_name='Ramesh Kumar',
        mobile_number='9876543210',
    )
    print('✅ Sample car owner created: car_owner_1 / car123')

# -- Sample driver
if not User.objects.filter(username='driver_1').exists():
    from drivers.models import Driver
    driver_user = User.objects.create_user(username='driver_1', password='driver123', role='driver')
    Driver.objects.create(
        user=driver_user,
        license_number='TN0120220012345',
        mobile_number='9123456780',
        address='Chennai, Tamil Nadu',
    )
    print('✅ Sample driver created: driver_1 / driver123')

# -- Sample customer
from customers.models import Customer
if not Customer.objects.exists():
    Customer.objects.create(
        name='John Doe',
        mobile_number='9000000001',
        email='john@example.com',
    )
    print('✅ Sample customer created')

print('\n🎉 Seed complete! Login at http://localhost:8000/admin/')
