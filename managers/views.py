from django.http import HttpRequest
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ApplicationPeriodSerializer, ApplicationPeriodUpdateSerializer

class 