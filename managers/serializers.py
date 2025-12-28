from rest_framework import serializers
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        new_access = refresh.access_token
        
        expires_at = timezone.now() + new_access.lifetime
        data["expires_at"] = expires_at.isoformat()
        
        return data

