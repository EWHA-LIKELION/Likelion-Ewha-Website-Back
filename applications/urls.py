from django.urls import path
from .views import ApplicantDetailView

app_name = 'applications'

urlpatterns = [
    path('applicant/<int:application_id>/', ApplicantDetailView.as_view()),
]