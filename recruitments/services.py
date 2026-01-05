from __future__ import annotations

from collections import defaultdict
from datetime import timedelta

from django.http import HttpRequest
from django.db.models import Max
from django.utils import timezone

from recruitments.models import RecruitmentSchedule, InterviewSchedule
from recruitments.serializers import InterviewGroupResponseSerializer
from utils.choices import PartChoices, InterviewMethodChoices

class InterviewScheduleService:

    SLOT_MINUTES = 30

    def __init__(self, request: HttpRequest):
        self.request = request
        self.serializer = None

    def get_interview_group_options(self) -> dict:
        part = self.request.query_params.get("part")
        interview_method = self.request.query_params.get("interview_method")

        self._validate_query_params(
            part=part,
            interview_method=interview_method
        )

        year = self._get_latest_year()

        schedules = (
            InterviewSchedule.objects.filter(
                recruitment_schedule_id=year,
                part=part,
                interview_method=interview_method,
            )
            .only("start", "end")
            .order_by("start")
        )

        if not schedules.exists():
            raise InterviewSchedule.DoesNotExist

        dates = self._build_dates_group(
            schedules=schedules
        )

        payload = {
            "year": year,
            "part": part,
            "interview_method": interview_method,
            "dates": dates
        }

        self.serializer = InterviewGroupResponseSerializer(
            data=payload
        )
        self.serializer.is_valid(
            raise_exception=True
        )
        return self.serializer.data

    def _validate_query_params(self, *, part: str | None, interview_method: str | None) -> None:
        if not part or not interview_method:
            raise ValueError("part and interview_method are required.")

        valid_parts = {
            choice.value
            for choice in PartChoices
        }
        valid_methods = {
            choice.value
            for choice in InterviewMethodChoices
        }

        if part not in valid_parts or interview_method not in valid_methods:
            raise ValueError("Invalid part or interview_method.")

    def _get_latest_year(self) -> int:
        year = RecruitmentSchedule.objects.aggregate(
            mx=Max("year")
        )["mx"]

        if year is None:
            raise RecruitmentSchedule.DoesNotExist

        return year

    def _to_kst_iso(self, dt) -> str:
        return timezone.localtime(dt).isoformat(
            timespec="seconds"
        )

    def _generate_slots(self, start_dt, end_dt):
        step = timedelta(
            minutes=self.SLOT_MINUTES
        )
        cur = start_dt

        # start 포함, end 미포함
        while cur < end_dt:
            yield cur
            cur += step

    def _build_dates_group(self, *, schedules) -> list[dict]:
        dates_map = defaultdict(
            lambda: {"am": [], "pm": []}
        )

        for schedule in schedules:
            start_dt = schedule.start
            end_dt = schedule.end

            if start_dt is None or end_dt is None or start_dt >= end_dt:
                continue

            for slot_dt in self._generate_slots(
                start_dt=start_dt,
                end_dt=end_dt
            ):
                local_dt = timezone.localtime(
                    slot_dt
                )
                date_key = local_dt.date().isoformat()

                if local_dt.hour < 12:
                    dates_map[date_key]["am"].append(
                        self._to_kst_iso(slot_dt)
                    )
                else:
                    dates_map[date_key]["pm"].append(
                        self._to_kst_iso(slot_dt)
                    )

        return [
            {"date": d, "am": v["am"], "pm": v["pm"]}
            for d, v in sorted(dates_map.items())
        ]

