"""Customers admin URL configs."""
from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView, CustomerAutoFillView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='admin-customer-list'),
    path('customers/<uuid:pk>/', CustomerDetailView.as_view(), name='admin-customer-detail'),
    path('customers/autofill/<str:customer_id>/', CustomerAutoFillView.as_view(), name='customer-autofill'),
]
