from django.utils import timezone
from rest_framework import serializers
from .models import ApplicationPeriod

class ApplicationPeriodSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationPeriod
        fields = ('id', 'recruit_year', 'part', 'start_datetime', 'end_datetime', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'recruit_year', 'part', 'status','created_at', 'updated_at')

    def get_status(self, obj: ApplicationPeriod):
        now = timezone.now()
        if now < obj.start_datetime:
            return {'code': 'PENDING', 'label': '모집 예정'}
        if obj.start_datetime <= now < obj.end_datetime:
            return {'code': 'ONGOING', 'label': '모집 중'}
        return {'code': 'CLOSED', 'label': '모집 마감'}

class ApplicationPeriodUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationPeriod
        fields = ('start_datetime', 'end_datetime')
    
    def validate(self, attrs):
        instance = getattr(self, "instance", None)

        start_datetime = attrs.get("start_datetime", instance.start_datetime if instance else None)
        end_datetime = attrs.get("end_datetime", instance.end_datetime if instance else None)

        if start_datetime and end_datetime and start_datetime >= end_datetime:
            raise serializers.ValidationError({'invalid_date':'지원 마감일은 지원 시작일 이후여야 합니다.'})
    
        return attrs