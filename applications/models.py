from django.db import models
from utils.choices import MethodChoices, PartChoices, StatusChoices

class Application(models.Model):
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
        max_length=7,
    )
    grade = models.CharField(
        help_text="학년",
        max_length=20,
    )
    method = models.CharField(
        help_text="면접 참여 방식",
        max_length=20,
        choices=MethodChoices.choices,
    )
    part = models.CharField(
        help_text="지원 파트",
        max_length=20,
        choices=PartChoices.choices,
    )
    status = models.CharField(
        help_text="합불 여부",
        max_length=10,
        choices=StatusChoices.choices,
        default="PENDING",
    )
    application_code = models.CharField(
        help_text="지원 코드",
        max_length=6,
    )
    created_at = models.DateTimeField(
        help_text="지원서 생성 일시",
        auto_now_add=True,
    )
    file_url = models.URLField(
        help_text="첨부파일",
        null=False,
        blank=False,
    )
    time = models.DateTimeField(
        help_text="면접 가능 시간",
        null=False,
        blank=False,
    )
    question_1 = models.CharField(
        help_text="자기소개서 1번 문항의 답변",
        max_length=500,
    )
    question_2 = models.CharField(
        help_text="자기소개서 2번 문항의 답변",
        max_length=500,
    )
    question_3 = models.CharField(
        help_text="자기소개서 3번 문항의 답변",
        max_length=500,
    )
    question_4 = models.CharField(
        help_text="자기소개서 4번 문항의 답변",
        max_length=500,
    )
    question_5 = models.TextField(
        help_text="자기소개서 5번 문항의 답변",
    )

    def __str__(self):
        return f"{self.student_number} {self.name} | {self.created_at.strftime('%Y-%m-%d %H:%M')}"
