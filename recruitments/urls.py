from django.urls import path
from .views import RecruitmentYearListView

app_name = 'recruitments'

urlpatterns = [
    path('application/years/', RecruitmentYearListView.as_view()),
]
