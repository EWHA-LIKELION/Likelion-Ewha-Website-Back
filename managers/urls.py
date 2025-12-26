from django.urls import path
from .views import *

app_name = 'managers'

urlpatterns = [
    path("200/", AlwaysOkView.as_view(), name="always-ok"),
]