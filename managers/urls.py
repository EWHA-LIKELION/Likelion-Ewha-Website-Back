from django.urls import path
from .views import *
from managers.views import CustomTokenRefreshView

app_name = 'managers'

urlpatterns = [
    path("auth/login/google/", GoogleAdminLoginView.as_view(), name="google-admin-login"),
    path("auth/access-token/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]