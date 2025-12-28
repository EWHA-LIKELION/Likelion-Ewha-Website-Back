from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'managers'

urlpatterns = [
    path("auth/login/google/", GoogleAdminLoginView.as_view(), name="google-admin-login"),
    path("auth/access-token/", TokenRefreshView.as_view(), name="token_refresh"),
]