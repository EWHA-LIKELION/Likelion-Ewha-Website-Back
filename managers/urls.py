from django.urls import path
from .views import ApplicationDetailView, ApplicationListView

app_name = 'managers'

urlpatterns = [
    path('applications/', ApplicationListView.as_view()),
    path('applications/<str:student_number>/', ApplicationDetailView.as_view()),
]