from django.urls import path
from .views import *

app_name = 'recruitments'

urlpatterns = [
  path(
        "application/interview-group/",
        InterviewGroupView.as_view(),
        name="interview-group"
    ),
]
