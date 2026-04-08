"""Commissions views — Admin list and default split configuration."""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Commission, CommissionDefault
from .serializers import CommissionSerializer, CommissionDefaultSerializer
from accounts.permissions import IsAdmin


class CommissionListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = CommissionSerializer
    queryset = Commission.objects.select_related('booking').all()
    filterset_fields = ['booking__vehicle', 'booking__driver']
    search_fields = ['booking__trip_no']


class CommissionDefaultView(APIView):
    """Get or update global commission split defaults."""
    permission_classes = [IsAdmin]

    def get(self, request):
        obj, _ = CommissionDefault.objects.get_or_create(pk=1)
        return Response(CommissionDefaultSerializer(obj).data)

    def patch(self, request):
        obj, _ = CommissionDefault.objects.get_or_create(pk=1)
        serializer = CommissionDefaultSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
