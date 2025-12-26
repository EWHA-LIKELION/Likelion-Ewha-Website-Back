from datetime import timedelta, timezone
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from utils.choices import PartChoices
from .models import ApplicationPeriod
from .serializers import ApplicationPeriodSerializer, ApplicationPeriodUpdateSerializer

class ApplicationPeriodService:
    def __init__(self, request:HttpRequest, recruit_year:int, part:str):
        self.request = request
        self.recruit_year = recruit_year
        self.part = part
        self.instance = get_object_or_404(ApplicationPeriod, recruit_year=recruit_year, part=part, error_message="지원서 모집 기간을 찾을 수 없어요.")
        self.serializer = ApplicationPeriodUpdateSerializer(self.instance, data=request.data)

    def get(self):
        return ApplicationPeriodSerializer(self.instance).data
    
    def patch(self):
        self.serializer.is_valid(raise_exception=True)
        instance = self.serializer.save()
        return instance
    
    def post_start_now(self):
        now = timezone.now()
        self.instance.
        324