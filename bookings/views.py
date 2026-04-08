"""Bookings views — Admin CRUD with filters, pending bookings, assignment."""
from rest_framework import generics
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer, BookingAssignSerializer
from accounts.permissions import IsAdmin
import django_filters.rest_framework as filters


class BookingFilter(filters.FilterSet):
    pickup_date_after = filters.DateFilter(field_name='pickup_date', lookup_expr='gte')
    pickup_date_before = filters.DateFilter(field_name='pickup_date', lookup_expr='lte')

    class Meta:
        model = Booking
        fields = ['vehicle', 'driver', 'customer', 'status', 'type_of_trip',
                  'pickup_date_after', 'pickup_date_before']


class BookingListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = BookingSerializer
    filterset_class = BookingFilter
    search_fields = ['trip_no', 'customer__name', 'customer__customer_id', 'pickup_location']
    ordering_fields = ['booking_date', 'pickup_date', 'fare']

    def get_queryset(self):
        return Booking.objects.select_related('customer', 'vehicle', 'driver').all()

    def create(self, request, *args, **kwargs):
        from rest_framework import status
        
        # Make a mutable copy of the frontend payload
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        
        # Extract custom nested customer data sent by the frontend
        customer_details = data.pop('customer_details', None)
        if customer_details and isinstance(customer_details, dict):
            from customers.models import Customer
            name = customer_details.get('name', 'Unknown')
            phone = customer_details.get('phone', '')
            
            # Find existing customer or auto-create a new one using the phone number
            customer_obj, created = Customer.objects.get_or_create(
                mobile_number=phone,
                defaults={'name': name}
            )
            data['customer'] = customer_obj.id
            data['is_new_customer'] = created
            
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()


class PendingBookingsView(generics.ListAPIView):
    """Bookings where driver has not been assigned."""
    permission_classes = [IsAdmin]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(driver__isnull=True).select_related('customer', 'vehicle')


class BookingAssignView(generics.UpdateAPIView):
    """Assign driver and/or car to a booking."""
    permission_classes = [IsAdmin]
    serializer_class = BookingAssignSerializer
    queryset = Booking.objects.all()
    http_method_names = ['patch']
