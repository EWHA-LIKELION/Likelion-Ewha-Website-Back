from django.db import models
from utils.choices import PartChoices, MethodChoices
from django.contrib.auth.models import AbstractUser

class Manager(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    ) 
    password = models.CharField(max_length=128)

class ApplicationPeriod(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"지원 기간 | "
            f"{self.start_datetime.strftime('%Y-%m-%d %H:%M')} ~ "
            f"{self.end_datetime.strftime('%Y-%m-%d %H:%M')}"
        )

class InterviewPeriod(models.Model):
    part = models.CharField(
        max_length=20,
        choices=PartChoices.choices
    )
    method = models.CharField(
        max_length=20,
        choices=MethodChoices.choices
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
