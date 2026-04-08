from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/admin/', include('accounts.admin_urls')),
    path('api/admin/', include('vehicles.urls')),
    path('api/admin/', include('drivers.urls')),
    path('api/admin/', include('customers.urls')),
    path('api/admin/', include('bookings.urls')),
    path('api/admin/', include('commissions.urls')),
    path('api/car/', include('vehicles.car_urls')),
    path('api/driver/', include('drivers.driver_urls')),
    path('api/admin/', include('trips.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
