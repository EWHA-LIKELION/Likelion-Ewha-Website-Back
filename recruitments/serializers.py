from rest_framework import serializers
from .models import Application
from utils.choices import InterviewMethodChoices, StatusChoices

class ApplicationSerializer(serializers.ModelSerializer):
    part = serializers.SerializerMethodField()
    interview_method = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    interview_at = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ("student_number", "part", "name", "interview_method", "interview_at", "status", "phone_number", "application_code",)

    def get_part(self, obj):
        return obj.get_part_display()
    
    def get_interview_method(self, obj):
        return obj.get_interview_method_display()
    
    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_interview_at(self, obj):
        if obj.interview_at is None:
            return "미확정"
        return obj.interview_at