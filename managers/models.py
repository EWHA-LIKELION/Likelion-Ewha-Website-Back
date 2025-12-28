from django.db import models
from utils.choices import PartChoices, InterviewMethodChoices

class RecruitmentSchedule(models.Model):
    year = models.PositiveSmallIntegerField(
        help_text="모집 연도",
        primary_key=True,
        editable=False,
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

class InterviewPeriod(models.Model):
    part = models.CharField(
        max_length=20,
        choices=PartChoices.choices
    )
    method = models.CharField(
        max_length=20,
        choices=InterviewMethodChoices.choices
    )
    time = models.DateTimeField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.get_part_display()} | "
            f"{self.get_method_display()} | "
            f"{self.time.strftime('%Y-%m-%d %H:%M')}"
        )
