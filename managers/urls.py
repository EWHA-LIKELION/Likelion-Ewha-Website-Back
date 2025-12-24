from django.urls import path
from .views import *

app_name = 'managers'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
]