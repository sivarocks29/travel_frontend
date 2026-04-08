"""
Analytics views for Admin Dashboard.
Provides totals, monthly, and yearly commission reports.
"""
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, TruncYear
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdmin
from bookings.models import Booking
from commissions.models import Commission


class DashboardAnalyticsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        total_bookings = Booking.objects.count()
        completed = Booking.objects.filter(status='completed').count()
        pending = Booking.objects.filter(driver__isnull=True).count()
        ongoing = Booking.objects.filter(status='ongoing').count()

        commission_totals = Commission.objects.aggregate(
            total=Sum('total_amount'),
            car=Sum('car_amount'),
            driver=Sum('driver_amount'),
            admin=Sum('admin_amount'),
        )

        return Response({
            'bookings': {
                'total': total_bookings,
                'completed': completed,
                'pending_assignment': pending,
                'ongoing': ongoing,
            },
            'commissions': {
                'total': commission_totals['total'] or 0,
                'car': commission_totals['car'] or 0,
                'driver': commission_totals['driver'] or 0,
                'admin': commission_totals['admin'] or 0,
            }
        })


class MonthlyAnalyticsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        year = request.query_params.get('year', None)
        bookings_qs = Booking.objects.annotate(month=TruncMonth('booking_date'))
        if year:
            bookings_qs = bookings_qs.filter(booking_date__year=year)

        monthly_bookings = bookings_qs.values('month').annotate(
            count=Count('id'),
            revenue=Sum('fare')
        ).order_by('month')

        monthly_commission = Commission.objects.annotate(month=TruncMonth('created_at'))
        if year:
            monthly_commission = monthly_commission.filter(created_at__year=year)
        monthly_commission = monthly_commission.values('month').annotate(
            car=Sum('car_amount'),
            driver=Sum('driver_amount'),
            admin=Sum('admin_amount'),
        ).order_by('month')

        return Response({
            'bookings': list(monthly_bookings),
            'commissions': list(monthly_commission),
        })


class YearlyAnalyticsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        yearly_bookings = Booking.objects.annotate(year=TruncYear('booking_date')).values('year').annotate(
            count=Count('id'),
            revenue=Sum('fare')
        ).order_by('year')

        yearly_commission = Commission.objects.annotate(year=TruncYear('created_at')).values('year').annotate(
            car=Sum('car_amount'),
            driver=Sum('driver_amount'),
            admin=Sum('admin_amount'),
        ).order_by('year')

        return Response({
            'bookings': list(yearly_bookings),
            'commissions': list(yearly_commission),
        })
