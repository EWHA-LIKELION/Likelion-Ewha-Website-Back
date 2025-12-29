from rest_framework import serializers
from .models import Application

class ApplicantSerializer(serializers.ModelSerializer):
    part = serializers.SerializerMethodField()
    method = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ("id", "part", "name", "method", "time", "status", "phone_number", "application_code",)

    def get_part(self, obj):
        return obj.get_part_display()
    
    def get_method(self, obj):
        return obj.get_method_display()
    
    def get_status(self, obj):
        return obj.get_status_display()