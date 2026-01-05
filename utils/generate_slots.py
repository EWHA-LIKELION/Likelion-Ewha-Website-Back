from datetime import timedelta
from recruitments.models import InterviewSlot, InterviewSchedule

SLOT_MINUTES = 30 

def generate_slots(schedule: InterviewSchedule):
    """
    InterviewSchedule(start~end) 기준으로 
    30분 단위 InterviewSlot 생성 
    """

    slots = []
    current = schedule.start

    while current < schedule.end:
        slots.append(
            InterviewSlot(
                interview_schedule=schedule,
                start=current,
                end=current + timedelta(minutes=SLOT_MINUTES),
            )
        )
        current += timedelta(minutes=SLOT_MINUTES)

    InterviewSlot.objects.bulk_create(slots)
    return len(slots)