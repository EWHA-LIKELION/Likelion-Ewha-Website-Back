from django.urls import path
from .views import ApplicantDetailView

app_name = 'managers'

urlpatterns = [
    path('<str:student_number>/', ApplicantDetailView.as_view()),
]