"""
Accounts views — Login, Logout (with driver timestamp), User management.
"""
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import LoginSerializer, UserSerializer
from .permissions import IsAdmin


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        tokens = serializer.get_tokens(user)

        # Track driver login timestamp
        if user.role == 'driver':
            from drivers.models import Driver, DriverLoginLog
            try:
                driver = user.driver_profile
                driver.is_logged_in = True
                driver.last_login_at = timezone.now()
                driver.save()
                # Log the event
                DriverLoginLog.objects.create(driver=driver, login_at=driver.last_login_at)
            except Exception:
                pass

        return Response(tokens, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

        # Track driver logout timestamp
        if request.user.role == 'driver':
            from drivers.models import Driver, DriverLoginLog
            try:
                driver = request.user.driver_profile
                driver.is_logged_in = False
                driver.last_logout_at = timezone.now()
                driver.save()
                # Update the latest log entry
                log = DriverLoginLog.objects.filter(driver=driver, logout_at__isnull=True).last()
                if log:
                    log.logout_at = driver.last_logout_at
                    log.save()
            except Exception:
                pass

        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email']
