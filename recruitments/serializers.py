from rest_framework import serializers
from .models import RecruitmentSchedule, InterviewSchedule
from utils.choices import PartChoices

class RecruitmentScheduleSerializer(serializers.ModelSerializer):
    """
    통합 모집 일정 조회/수정에서 RecruitmentSchedule 필드를 제공합니다.
    """
    class Meta:
        model = RecruitmentSchedule
        fields = (
            'year', 'application_start', 'application_end',
            'first_result_start', 'first_result_end',
            'interview_start', 'interview_end',
            'final_result_start', 'final_result_end',
        )
        read_only_fields = (
            'year',
            'first_result_end',
            'interview_start',
            'interview_end',
        )

class InterviewScheduleSerializer(serializers.ModelSerializer):
    """
    통합 모집 일정 조회/수정에서 InterviewSchedule 필드를 part별로 그룹화하여 제공합니다.
    """
    class Meta:
        model = InterviewSchedule
        fields = (
            'id', 'part', 'start', 'end', 'interview_method', 'interview_location',
        )
        read_only_fields = ('id',)
    
    def validate(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')

        if start and end:
            if start >= end:
                raise serializers.ValidationError(
                    {"time": "면접 시작 시간은 종료 시간보다 이전이어야 합니다."}
                )
            if start.date() != end.date():
                raise serializers.ValidationError(
                    {"date": "면접 시작/종료는 같은 날짜여야 합니다."}
                )
        return attrs

class CombinedScheduleSerializer(serializers.Serializer):
    """
    모집 일정 + 면접 일정 통합 조회/수정 API에서 사용합니다.
    """
    recruitment_schedule = RecruitmentScheduleSerializer(required=False)
    interview_schedules = serializers.DictField(required=False)

    def validate_interview_schedules(self, value):
        valid_parts = {k for k, _ in PartChoices.choices}

        for part, schedules in value.items():
            if part not in valid_parts:
                raise serializers.ValidationError({part: "유효하지 않은 파트입니다."})

            if not isinstance(schedules, list):
                raise serializers.ValidationError({part: "리스트 형태여야 합니다."})
            
            serializer = InterviewScheduleSerializer(data=schedules, many=True)
            serializer.is_valid(raise_exception=True)

            value[part] = serializer.validated_data
        return value
