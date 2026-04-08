"""Accounts admin URLs — analytics, driver logs, user list."""
from django.urls import path
from .views import UserListView
from .analytics_views import DashboardAnalyticsView, MonthlyAnalyticsView, YearlyAnalyticsView
from drivers.views import DriverLoginLogView

urlpatterns = [
    path('users/', UserListView.as_view(), name='admin-users'),
    path('analytics/dashboard/', DashboardAnalyticsView.as_view(), name='analytics-dashboard'),
    path('analytics/monthly/', MonthlyAnalyticsView.as_view(), name='analytics-monthly'),
    path('analytics/yearly/', YearlyAnalyticsView.as_view(), name='analytics-yearly'),
    path('driver-logs/', DriverLoginLogView.as_view(), name='driver-logs'),
]
