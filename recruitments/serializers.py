from rest_framework import serializers
from .models import Application
from utils.choices import InterviewMethodChoices, StatusChoices
    
class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("interview_method", "status")
    #면접 방식 수정(기획에서 빠짐)
    def validate_interview_method(self, value):
        if value not in InterviewMethodChoices.values:
            raise serializers.VallidationError("유효하지 않은 항목")
        return value
    #합격 여부 상태
    def validate_status(self, value):
        if value not in StatusChoices.values:
            raise serializers.ValidationError("유효하지 않은 항목")
        return value