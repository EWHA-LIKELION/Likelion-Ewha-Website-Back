from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import ApplicationPeriod, InterviewPeriod, InterviewSchedule

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

class InterviewPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewPeriod
        fields = ('id', 'recruit_year', 'part', 'start_date', 'end_date', 'created_at', 'updated_at')
        read_only_fields = ('id', 'recruit_year', 'part', 'created_at', 'updated_at')

    def validate(self, attrs):
        instance = getattr(self, "instance", None)

        start_date = attrs.get("start_date", instance.start_date if instance else None)
        end_date = attrs.get("end_date", instance.end_date if instance else None)

        # start만 들어오면 end = start + 7일
        if "start_date" in attrs and attrs.get("start_date") and "end_date" not in attrs:
            attrs["end_date"] = attrs["start_date"] + timedelta(days=7)
            start_date = attrs["start_date"]
            end_date = attrs["end_date"]

        # end만 들어오면 start = end - 7일
        if "end_date" in attrs and attrs.get("end_date") and "start_date" not in attrs:
            attrs["start_date"] = attrs["end_date"] - timedelta(days=7)
            start_date = attrs["start_date"]
            end_date = attrs["end_date"]

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"invalid_date": "면접 시작일은 종료일보다 늦을 수 없습니다."})
        
        return attrs

# 면접 슬롯 고정값 (오전)
MORNING_SLOTS_GUI = ("09:00", "09:30", "10:00", "10:30", "11:00", "11:30")

# 면접 슬롯 고정값 (오후)
AFTERNOON_SLOTS_GUI = (
    "12:00", "12:30",
    "01:00", "01:30", "02:00", "02:30", "03:00", "03:30",
    "04:00", "04:30", "05:00", "05:30",
    "06:00", "06:30", "07:00", "07:30",
    "08:00", "08:30", "09:00", "09:30",
)

# GUI 형식의 시간을 시, 분으로 파싱
def _parse_gui_time(s: str) -> tuple[int, int]:
    if not isinstance(s, str) or ":" not in s:
        raise serializers.ValidationError({"invalid_format": "시간 형식은 'H:MM' 또는 'HH:MM' 이어야 합니다."})

    h_str, m_str = s.split(":", 1)
    if not (h_str.isdigit() and m_str.isdigit()):
        raise serializers.ValidationError({"invalid_format": "시간은 숫자여야 합니다."})

    h = int(h_str)
    m = int(m_str)
    if m not in (0, 30):
        raise serializers.ValidationError({"invalid_format": "분(minute)은 00 또는 30만 허용합니다."})

    return h, m

# GUI 형식의 시간을 24시간 형식으로 변환
def gui_to_24h(gui: str, period: str) -> str:
    if period not in ("AM", "PM"):
        raise serializers.ValidationError({"invalid_period": [period]})
    
    allowed = MORNING_SLOTS_GUI if period == "AM" else AFTERNOON_SLOTS_GUI
    if gui not in allowed:
        raise serializers.ValidationError({"invalid_time": [gui]})
    
    h, m = _parse_gui_time(gui)

    if period == "PM":
        if h == 12:
            pass
        elif 1 <= h <= 9:
            h += 12
        else:
            raise serializers.ValidationError({"invalid_time": [gui]})
    
    return f"{h:02d}:{m:02d}"

# 24시간 형식의 시간을 GUI 형식으로 변환
def to_gui_from_24h(t24: str) -> str:
    if not isinstance(t24, str) or ":" not in t24:
        raise serializers.ValidationError({"invalid_time": [t24]})

    hh, mm = t24.split(":", 1)
    if not (hh.isdigit() and mm.isdigit()):
        raise serializers.ValidationError({"invalid_time": [t24]})
    
    h = int(hh)
    m = int(mm)
    if m not in (0, 30):
        raise serializers.ValidationError({"invalid_time": [t24]})

    if not ((9 <= h <= 11) or (h == 12) or (13 <= h <= 21)):
        raise serializers.ValidationError({"invalid_time": [t24]})
    
    # 9시~12시대
    if 9 <= h <= 12:
        return f"{h:02d}:{m:02d}"
    # 13시~21시대
    return f"{h - 12:02d}:{m:02d}"

class InterviewScheduleSerializer(serializers.ModelSerializer):
    slots_gui = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField()),
        write_only=True,
        required=False,
    )
    slots = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = InterviewSchedule
        fields = ('id', 'recruit_year', 'part', 'method', 'date', 'slots_gui', 'slots', 'created_at', 'updated_at')
        read_only_fields = ('id', 'recruit_year', 'part', 'method', 'created_at', 'updated_at')

    def validate(self, attrs):
        if "slots_gui" in attrs:
            payload = attrs.get("slots_gui") or {}
            
            am_list = payload.get("AM", [])
            pm_list = payload.get("PM", [])

            if not isinstance(am_list, list) or not all(isinstance(x, str) for x in am_list):
                raise serializers.ValidationError({"slots_gui": {"AM": "문자열 배열이어야 합니다."}})
            if not isinstance(pm_list, list) or not all(isinstance(x, str) for x in pm_list):
                raise serializers.ValidationError({"slots_gui": {"PM": "문자열 배열이어야 합니다."}})

            if len(am_list) + len(pm_list) == 0:
                raise serializers.ValidationError({"slots_gui": "최소 1개 이상의 시간을 선택해야 합니다."})
            
            unknown_am = [t for t in am_list if t not in MORNING_SLOTS_GUI]
            unknown_pm = [t for t in pm_list if t not in AFTERNOON_SLOTS_GUI]
            if unknown_am or unknown_pm:
                raise serializers.ValidationError({"slots_gui": {"invalid_time": {"AM": unknown_am, "PM": unknown_pm}}})

            normalized_24h = []
            for t in am_list:
                normalized_24h.append(gui_to_24h(t, "AM"))
            for t in pm_list:
                normalized_24h.append(gui_to_24h(t, "PM"))

            normalized_24h = sorted(set(normalized_24h))

            attrs["slots_raw"] = normalized_24h
            attrs.pop("slots_gui", None)

        return attrs

    def create(self, validated_data):
        slots = validated_data.pop("slots_raw", None)
        if slots is not None:
            validated_data["slots"] = slots
        return super().create(validated_data)

    def update(self, instance, validated_data):
        slots = validated_data.pop("slots_raw", None)
        if slots is not None:
            validated_data["slots"] = slots
        return super().update(instance, validated_data)
    
    def get_slots(self, obj: InterviewSchedule):
        if not isinstance(obj.slots, list):
            return {"AM": [], "PM": []}

        am, pm = [], []
        for t24 in obj.slots:
            if not isinstance(t24, str) or ":" not in t24:
                continue

            hh, mm = t24.split(":", 1)
            if not (hh.isdigit() and mm.isdigit()):
                continue

            h = int(hh)

            gui = to_gui_from_24h(t24)

            # 09~11 => AM, 12~21 => PM
            if 9 <= h <= 11:
                am.append(gui)
            else:
                pm.append(gui)

        return {"AM": am, "PM": pm}