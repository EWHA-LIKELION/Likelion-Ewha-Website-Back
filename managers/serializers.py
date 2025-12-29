from rest_framework import serializers
from applications.models import Application
from utils.choices import InterviewMethodChoices, StatusChoices

class ApplicationSerializer(serializers.ModelSerializer):
    part = serializers.SerializerMethodField()
    interview_method = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ("student_number", "part", "name", "interview_method", "interview_at", "status", "phone_number", "application_code",)

    def get_part(self, obj):
        return obj.get_part_display()
    
    def get_interview_method(self, obj):
        return obj.get_interview_method_display()
    
    def get_status(self, obj):
        return obj.get_status_display()
    
class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("interview_method", "status")

    def validate_interview_method(self, value):
        if value not in InterviewMethodChoices.values:
            raise serializers.VallidationError("유효하지 않은 항목")
        return value
    
    def validate_status(self, value):
        if value not in StatusChoices.values:
            raise serializers.ValidationError("유효하지 않은 항목")
        return value