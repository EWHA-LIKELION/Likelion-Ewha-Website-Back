from django.urls import path
from .views import *

app_name = 'recruitments'

urlpatterns = [
    path("recruitment-schedule/", CombinedScheduleView.as_view()),
    path("application/", ApplicationView.as_view())
]
