from django.urls import path
from .views import *

app_name = 'recruitments'

urlpatterns = [
    path("recruitment-schedules/", CombinedScheduleView.as_view()),
]