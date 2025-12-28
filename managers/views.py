from django.shortcuts import render
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import CustomTokenRefreshSerializer
from .api_base import ManagerBaseAPIView

from .models import AllowedManagerEmail
from .google import verify_google_id_token

User = get_user_model()

@method_decorator(csrf_exempt, name="dispatch")
class GoogleAdminLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] # 로그인 이전엔 토큰 검사 X

    def post(self, request):
        raw_id_token = request.data.get("id_token")
        if not raw_id_token:
            return Response({"detail": "id_token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = verify_google_id_token(raw_id_token)
        except Exception:
            return Response({"detail": "Invalid Google token."}, status=status.HTTP_401_UNAUTHORIZED)

        email = (payload.get("email") or "").strip().lower()
        email_verified = payload.get("email_verified", False)

        if not email:
            return Response({"detail": "Google email not found."}, status=status.HTTP_400_BAD_REQUEST)

        if not email_verified:
            return Response({"detail": "Google email is not verified."}, status=status.HTTP_403_FORBIDDEN)

        allowed = AllowedManagerEmail.objects.filter(email=email, is_active=True).exists()
        if not allowed:
            return Response({"detail": "Not allowed manager."}, status=status.HTTP_403_FORBIDDEN)

        # 유저 생성/조회
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "is_active": True,
                "is_staff": True,      # 관리자 로그인 목적
                "is_superuser": False, 
            },
        )

        if not user.is_staff:
            user.is_staff = True
        if not user.is_active:
            user.is_active = True
        user.save(update_fields=["is_staff", "is_active"])

        # JWT 발급
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access_lifetime = access.lifetime

        return Response(
            {
                "access": str(access),
                "expires_at": (timezone.now() + access_lifetime).isoformat(),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_staff": user.is_staff,
                },
            },
            status=status.HTTP_200_OK,
        )

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer