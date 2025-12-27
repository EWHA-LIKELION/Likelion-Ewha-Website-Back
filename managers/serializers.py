from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from .models import ApplicationPeriod

DISPLAY_FMT = "%Y.%m.%d %H:%M"

class ApplicationPeriodSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)

    start_datetime = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)
    end_datetime = serializers.CharField(required=False, allow_null=True, allow_blank=True, write_only=True)

    start_display = serializers.SerializerMethodField()
    end_display = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationPeriod
        fields = ('id', 'recruit_year', 'part', 'start_datetime', 'start_display', 'end_datetime', 'end_display', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'recruit_year', 'part', 'status','created_at', 'updated_at')

    def _parse(self, value: str):
        if value is None:
            return None
        value = value.strip()
        if value == "":
            return None
        
        try:
            naive = datetime.strptime(value, DISPLAY_FMT)
        except ValueError:
            raise serializers.ValidationError(
                f"날짜 형식이 올바르지 않아요. 예) 2026.03.01 10:00"
            )
        return timezone.make_aware(naive, timezone.get_current_timezone())
    
    def validate(self, attrs):
        instance = getattr(self, "instance", None)

        if "start_datetime" in attrs:
            attrs["start_datetime"] = self._parse(attrs["start_datetime"])
        if "end_datetime" in attrs:
            attrs["end_datetime"] = self._parse(attrs["end_datetime"])

        start_datetime = attrs.get("start_datetime", instance.start_datetime if instance else None)
        end_datetime = attrs.get("end_datetime", instance.end_datetime if instance else None)

        if start_datetime and end_datetime and start_datetime >= end_datetime:
            raise serializers.ValidationError({'invalid_date':'지원 마감일은 지원 시작일 이후여야 합니다.'})
    
        return attrs

    def get_start_display(self, obj):
        if not obj.start_datetime:
            return None
        return timezone.localtime(obj.start_datetime).strftime(DISPLAY_FMT)

    def get_end_display(self, obj):
        if not obj.end_datetime:
            return None
        return timezone.localtime(obj.end_datetime).strftime(DISPLAY_FMT)

    def get_status(self, obj: ApplicationPeriod):
        if not obj.start_datetime or not obj.end_datetime:
            return {"code": "UNSET", "label": "미설정"}
        
        now = timezone.localtime(timezone.now())
        start_datetime = timezone.localtime(obj.start_datetime)
        end_datetime = timezone.localtime(obj.end_datetime)

        if now < start_datetime:
            return {'code': 'PENDING', 'label': '모집 예정'}
        if start_datetime <= now < end_datetime:
            return {'code': 'ONGOING', 'label': '모집 중'}
        return {'code': 'CLOSED', 'label': '모집 마감'}