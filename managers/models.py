from django.db import models
from utils.choices import InterviewMethodChoices

class RecruitmentSchedule(models.Model):
    year = models.PositiveSmallIntegerField(
        help_text="모집 연도",
        primary_key=True,
    )
    application_start = models.DateTimeField(
        help_text="서류 지원 기간 시작",
    )
    application_end = models.DateTimeField(
        help_text="서류 지원 기간 종료",
    )
    application_result_start = models.DateTimeField(
        help_text="서류 합격자 발표 시작",
    )
    # 서류 합격자 발표 종료는 지정하지 않음
    interview_start = models.DateTimeField(
        help_text="면접 기간 시작",
    )
    interview_end = models.DateTimeField(
        help_text="면접 기간 종료",
    )
    interview_result_start = models.DateTimeField(
        help_text="최종 합격자 발표 시작",
    )
    interview_result_end = models.DateTimeField(
        help_text="최종 합격자 발표 종료",
    )

    def __str__(self):
        return f"{self.year}년 모집 일정"

class InterviewSchedule(models.Model):
    recruitment_schedule = models.ForeignKey(
        help_text="특정 연도의 모집 일정",
        to=RecruitmentSchedule,
        on_delete=models.CASCADE,
        related_name="interview_schedules",
    )
    start = models.DateTimeField(
        help_text="특정 날짜의 면접 시작 시각",
    )
    end = models.DateTimeField(
        help_text="특정 날짜의 면접 종료 시각",
    )
    interview_method = models.CharField(
        help_text="면접 방식",
        max_length=7,
        choices=InterviewMethodChoices.choices,
    )

    def __str__(self):
        return f"{self.recruitment_schedule.year}년 면접 일정 | {self.start.strftime('%Y-%m-%d %H:%M')}-{self.end.strftime('%Y-%m-%d %H:%M')} ({self.get_interview_method_display()})"
