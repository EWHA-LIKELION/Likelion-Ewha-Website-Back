from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import localtime
from utils.choices import PartChoices, InterviewMethodChoices, StatusChoices

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
    completed_prerequisites = ArrayField(
        help_text="선수강 강의 이수 내역",
        base_field=models.URLField(),
        size=3,
        default=list,
    )
    portfolios = ArrayField(
        help_text="포트폴리오",
        base_field=models.URLField(),
        size=3,
        default=list,
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
        max_length=8,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    def __str__(self):
        return f"{self.student_number} {self.name} ({localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S %Z')})"
