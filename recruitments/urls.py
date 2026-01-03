from django.urls import path
from .views import ApplicationListView

app_name = 'recruitments'

urlpatterns = [
    path('application/', ApplicationListView.as_view()),
]
