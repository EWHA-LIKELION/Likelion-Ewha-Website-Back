from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import localtime
from utils.choices import InterviewMethodChoices

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    ) 
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    def __str__ (self):
        return self.email

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
        help_text="면접 시작 일시 (end와 같은 날)",
    )
    end = models.DateTimeField(
        help_text="면접 종료 일시 (start와 같은 날)",
    )
    interview_method = models.CharField(
        help_text="면접 방식",
        max_length=7,
        choices=InterviewMethodChoices.choices,
    )

    def __str__(self):
        return f"{self.recruitment_schedule.year}년 면접 일정 | {localtime(self.start).strftime('%Y-%m-%d %H:%M:%S %Z')} ~ {localtime(self.end).strftime('%Y-%m-%d %H:%M:%S %Z')} ({self.get_interview_method_display()})"
