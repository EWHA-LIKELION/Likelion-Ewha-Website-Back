from django.db import models
from utils.choices import PartChoices, MethodChoices

class ApplicationPeriod(models.Model):
    recruit_year = models.IntegerField()
    part = models.CharField(
        max_length=20,
        choices=PartChoices.choices
    )
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
    recruit_year = models.IntegerField()
    part = models.CharField(
        max_length=20,
        choices=PartChoices.choices
    )
    method = models.CharField(
        max_length=20,
        choices=MethodChoices.choices
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.recruit_year}년 {self.get_part_display()} | {self.get_method_display()} | {self.start_date} ~ {self.end_date}"

class InterviewSchedule(models.Model):
    recruit_year = models.IntegerField()
    part = models.CharField(
        max_length=20,
        choices=PartChoices.choices
    )
    method = models.CharField(
        max_length=20,
        choices=MethodChoices.choices
    )
    date = models.DateField()
    slots = models.JSONField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.recruit_year}년 {self.get_part_display()} | {self.get_method_display()} | {self.date}"