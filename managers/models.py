from django.db import models
from utils.choices import PartChoices, MethodChoices

class ApplicationPeriod(models.Model):
    recruit_year = models.IntegerField()
    part = models.CharField(
        max_length=20,
        choices=PartChoices.choices
    )
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recruit_year", "part"],
                name="uniq_application_period_year_part",
            )
        ]

    def __str__(self):
        start = self.start_datetime.strftime("%Y-%m-%d %H:%M") if self.start_datetime else "미설정"
        end = self.end_datetime.strftime("%Y-%m-%d %H:%M") if self.end_datetime else "미설정"
        return f"{self.id} | {self.recruit_year}년 {self.get_part_display()} | {start} ~ {end}"

class InterviewPeriod(models.Model):
    recruit_year = models.IntegerField()
    part = models.CharField(
        max_length=20,
        choices=PartChoices.choices
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recruit_year", "part"],
                name="uniq_interview_period_year_part",
            )
        ]

    def __str__(self):
        start = self.start_date.isoformat() if self.start_date else "미설정"
        end = self.end_date.isoformat() if self.end_date else "미설정"
        return f"{self.id} | {self.recruit_year}년 {self.get_part_display()} | {start} ~ {end}"

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recruit_year", "part", "method", "date"],
                name="uniq_interview_schedule_year_part_method_date",
            )
        ]

    def __str__(self):
        return f"{self.id} | {self.recruit_year}년 {self.get_part_display()} | {self.get_method_display()} | {self.date}"