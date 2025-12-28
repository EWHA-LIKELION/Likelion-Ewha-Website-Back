from django.urls import path
from .views import *

app_name = 'managers'

urlpatterns = [
    path("application-period/", ApplicationPeriodView.as_view()),
    path("application-period/start/", ApplicationPeriodStartView.as_view()),
    path("application-period/end/", ApplicationPeriodEndView.as_view()),
    path("interview-period/", InterviewPeriodView.as_view()),
    path("interview-schedules/", InterviewScheduleView.as_view()),
    path("interview-schedules/<int:pk>/", InterviewScheduleDetailView.as_view()),
]