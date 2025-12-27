from django.urls import path
from .views import *

app_name = 'managers'

urlpatterns = [
    path("application-period/", ApplicationPeriodView.as_view()),
    path("application-period/start/", ApplicationPeriodStartView.as_view()),
    path("application-period/end/", ApplicationPeriodEndView.as_view()),
]