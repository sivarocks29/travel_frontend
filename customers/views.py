"""Customers views — Admin CRUD + auto-fill endpoint."""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer, CustomerAutoFillSerializer
from accounts.permissions import IsAdmin


class CustomerListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    filterset_fields = []
    search_fields = ['name', 'mobile_number', 'customer_id']


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerAutoFillView(APIView):
    """Return customer data by customer_id — used in booking form auto-fill."""
    permission_classes = [IsAdmin]

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            return Response(CustomerAutoFillSerializer(customer).data)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
