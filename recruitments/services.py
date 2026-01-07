from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.db.models.functions import Cast
from django.db.models import DateField, Min, Max, Value
from .models import RecruitmentSchedule, InterviewSchedule
from .serializers import RecruitmentScheduleSerializer, InterviewScheduleSerializer

class RecruitmentScheduleService:
    def __init__(self, request:HttpRequest, year:int|None=None):
        instance = get_object_or_404(RecruitmentSchedule, year=year) if year else None
        self.request = request
        self.instance = instance
    
    def group_interviews(self) -> dict:
        """
        특정 모집 연도에 속한 모든 면접 일정을 파트별로 그룹화합니다.
        """
        interview_schedules = InterviewSchedule.objects.filter(
            recruitment_schedule = self.instance
        ).order_by('part', 'start')

        grouped: dict[str, list] = {}
        data = InterviewScheduleSerializer(interview_schedules, many=True).data

        for row in data:
            grouped.setdefault(row['part'], []).append(row)
        
        return grouped
    
    def calc_interview_period(self) -> None:
        """
        파트별 면접 일정을 바탕으로 모집 일정의 interview_start/end을 자동 계산합니다.
        """
        interview_period = InterviewSchedule.objects.filter(
            recruitment_schedule=self.instance
        )

        if not interview_period.exists():
            self.instance.interview_start = None
            self.instance.interview_end = None
            self.instance.save(update_fields=["interview_start", "interview_end"])
            return
        
        aggregates = interview_period.aggregate(
            min_day=Min(Cast("start", output_field=DateField())),
            max_day=Max(Cast("start", output_field=DateField())),
        )
        self.instance.interview_start = aggregates["min_day"]
        self.instance.interview_end = aggregates["max_day"]
        self.instance.save(update_fields=["interview_start", "interview_end"])
    
    def get(self) -> dict:
        return {
            'recruitment_schedule': RecruitmentScheduleSerializer(self.instance).data,
            'interview_schedules': self.group_interviews(),
        }

    def post(self, year:int, validated_data: dict) -> dict:
        with transaction.atomic():
            recruit_schedule = validated_data["recruitment_schedule"]
            if recruit_schedule is None:
                raise ValueError("모집 일정 데이터가 필요합니다.")
        
            if RecruitmentSchedule.objects.filter(year=year).exists():
                raise ValueError("이미 해당 연도의 모집 일정이 존재합니다.")
            
            
            recruit_schedule["first_result_end"] = recruit_schedule["final_result_start"]
        
            # 모집 일정 생성
            self.instance = RecruitmentSchedule.objects.create(
                year=year,
                **recruit_schedule
            )

            # 면접 일정 생성
            interview_schedules_part = validated_data.get("interview_schedules")
            if interview_schedules_part:
                for part, items in interview_schedules_part.items():
                    objs = [
                        InterviewSchedule(
                            recruitment_schedule=self.instance,
                            part=part,
                            start=itv["start"],
                            end=itv["end"],
                            interview_method=itv["interview_method"],
                            interview_location=itv.get("interview_location") or None,
                        )
                        for itv in items
                    ]
                    if objs:
                        InterviewSchedule.objects.bulk_create(objs)

                self.calc_interview_period()

        return self.get()
    
    def patch(self, validated_data: dict) -> dict:
        with transaction.atomic():
            # 모집 일정 수정
            recruitment_schedule = validated_data.get('recruitment_schedule')
            if recruitment_schedule is not None:
                serializer = RecruitmentScheduleSerializer(
                    self.instance,
                    data=recruitment_schedule,
                    partial=True,
                )
                serializer.is_valid(raise_exception=True)
                self.instance = serializer.save()

                # 1차 합격자 발표 종료일 = 최종 합격자 발표 시작일 (first_result_end = final_result_start)
                if "final_result_start" in serializer.validated_data:
                    self.instance.first_result_end = self.instance.final_result_start
                    self.instance.save(update_fields=['first_result_end'])
            
            # 면접 일정 수정
            interview_schedules_part = validated_data.get('interview_schedules')
            if interview_schedules_part is not None:
                for part, items in interview_schedules_part.items():
                    InterviewSchedule.objects.filter(
                        recruitment_schedule=self.instance,
                        part=part,
                    ).delete()

                    objs = [
                        InterviewSchedule(
                            recruitment_schedule=self.instance,
                            part=part,
                            start=itv["start"],
                            end=itv["end"],
                            interview_method=itv["interview_method"],
                            interview_location=itv.get("interview_location") or None,
                        )
                        for itv in items
                    ]
                    if objs:
                        InterviewSchedule.objects.bulk_create(objs)
                self.calc_interview_period()

        return self.get()