from django.db import models
from utils.choices import MethodChoices, PartChoices, StatusChoices

class Application(models.Model):
    name = models.CharField(
        max_length=30,
    )
    phone_number = models.CharField(
        max_length=13,
    )
    birthday = models.DateField()
    department = models.CharField(
        max_length=50,
    )
    student_number = models.CharField(
        max_length=7,
    )
    grade = models.CharField(
        max_length=20,
    )
    method = models.CharField(
        max_length=20,
        choices=MethodChoices.choices,
    )
    part = models.CharField(
        max_length=20,
        choices=PartChoices.choices,
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default="PENDING",
    )
    application_code = models.CharField(
        max_length=6,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    file_url = models.URLField(
        null=False,
        blank=False,
    )
    time = models.DateTimeField(
        null=False,
        blank=False,
    )
    question_1 = models.TextField(
        max_length=500,
    )
    question_2 = models.TextField(
        max_length=500,
    )
    question_3 = models.TextField(
        max_length=500,
    )
    question_4 = models.TextField(
        max_length=500,
    )
    question_5 = models.TextField(
        max_length=500,
    )

    def __str__(self):
        return f"{self.student_number} {self.name} | {self.created_at.strftime('%Y-%m-%d %H:%M')}"
