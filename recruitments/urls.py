from django.urls import path
from .views import ApplicationDetailView

app_name = 'recruitments'

urlpatterns = [
    path('application/<str:student_number>/', ApplicationDetailView.as_view()),
]
