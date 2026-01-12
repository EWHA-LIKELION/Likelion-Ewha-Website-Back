from django.urls import path
from .views import *

app_name = 'recruitments'

urlpatterns = [
    path('application/<str:student_number>', ApplicationByStudentNumberView.as_view()),
    path("application/", ApplicationView.as_view())
]