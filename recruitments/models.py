from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import localtime
from utils.choices import PartChoices, InterviewMethodChoices, StatusChoices

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
    first_result_start = models.DateTimeField(
        help_text="1차 합격자 발표 시작",
    )
    first_result_end = models.DateTimeField(
        help_text="1차 합격자 발표 종료",
    )
    interview_start = models.DateField(
        help_text="면접 기간 시작",
        null=True,
        blank=True,
    )
    interview_end = models.DateField(
        help_text="면접 기간 종료",
        null=True,
        blank=True,
    )
    final_result_start = models.DateTimeField(
        help_text="최종 합격자 발표 시작",
    )
    final_result_end = models.DateTimeField(
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
    part = models.CharField(
        help_text="파트",
        max_length=9,
        choices=PartChoices.choices,
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
    interview_location = models.CharField(
        help_text="면접 장소 또는 온라인 면접 링크",
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.recruitment_schedule.year}년 면접 일정 | {localtime(self.start).strftime('%Y-%m-%d %H:%M:%S %Z')} ~ {localtime(self.end).strftime('%Y-%m-%d %H:%M:%S %Z')} ({self.get_interview_method_display()})"

class Application(models.Model):
    # 인적사항
    name = models.CharField(
        help_text="이름",
        max_length=30,
    )
    phone_number = models.CharField(
        help_text="전화번호",
        max_length=13,
    )
    birthday = models.DateField(
        help_text="생년월일",
    )
    department = models.CharField(
        help_text="학과",
        max_length=50,
    )
    student_number = models.CharField(
        help_text="학번",
        primary_key=True,
        max_length=7,
    )
    grade = models.CharField(
        help_text="학년",
        max_length=20,
    )

    # 면접
    interview_method = models.CharField(
        help_text="면접 참여 방식",
        max_length=7,
        choices=InterviewMethodChoices.choices,
    )
    interview_available_times = ArrayField(
        help_text="면접 가능 시간",
        base_field=models.DateTimeField(),
        default=list,
    )
    interview_at = models.DateTimeField(
        help_text="면접 확정 시간",
        null=True,
        blank=True,
    )

    # 자기소개
    part = models.CharField(
        help_text="지원 파트",
        max_length=9,
        choices=PartChoices.choices,
    )
    personal_statement_1 = models.CharField(
        help_text="자기소개 1번 문항의 답변",
        max_length=500,
    )
    personal_statement_2 = models.CharField(
        help_text="자기소개 2번 문항의 답변",
        max_length=500,
    )
    personal_statement_3 = models.CharField(
        help_text="자기소개 3번 문항의 답변",
        max_length=500,
    )
    personal_statement_4 = models.CharField(
        help_text="자기소개 4번 문항의 답변",
        max_length=500,
    )
    personal_statement_5 = models.TextField(
        help_text="자기소개 5번 문항의 답변",
    )
    completed_prerequisite_1 = models.ImageField(
        help_text="선수강 강의 이수 내역",
        upload_to="application/completed_prerequisite",
        null=True,
        blank=True,
    )
    completed_prerequisite_2 = models.ImageField(
        help_text="선수강 강의 이수 내역",
        upload_to="application/completed_prerequisite",
        null=True,
        blank=True,
    )
    completed_prerequisite_3 = models.ImageField(
        help_text="선수강 강의 이수 내역",
        upload_to="application/completed_prerequisite",
        null=True,
        blank=True,
    )
    portfolio_1 = models.FileField(
        help_text="포트폴리오",
        upload_to="application/portfolio",
        null=True,
        blank=True,
    )
    portfolio_2 = models.FileField(
        help_text="포트폴리오",
        upload_to="application/portfolio",
        null=True,
        blank=True,
    )
    portfolio_3 = models.FileField(
        help_text="포트폴리오",
        upload_to="application/portfolio",
        null=True,
        blank=True,
    )

    # 그외
    created_at = models.DateTimeField(
        help_text="지원서 추가 일시",
        auto_now_add=True,
    )
    application_code = models.CharField(
        help_text="지원 코드",
        max_length=10,
    )
    status = models.CharField(
        help_text="합불 여부",
        max_length=14,
        choices=StatusChoices.choices,
        default=StatusChoices.FIRST_PENDING,
    )

    class Meta:
        indexes = [
            models.Index(fields=["status"], name="application_status_idx")
        ]

    def __str__(self):
        return f"{self.student_number} {self.name} ({localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S %Z')})"
