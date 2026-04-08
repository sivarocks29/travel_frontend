"""Commissions admin URL configs."""
from django.urls import path
from .views import CommissionListView, CommissionDefaultView

urlpatterns = [
    path('commissions/', CommissionListView.as_view(), name='admin-commission-list'),
    path('commissions/defaults/', CommissionDefaultView.as_view(), name='admin-commission-defaults'),
]
