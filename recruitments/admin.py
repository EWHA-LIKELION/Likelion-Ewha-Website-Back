from django.contrib import admin
from .models import RecruitmentSchedule, InterviewSchedule, Application, InterviewSlot

admin.site.register(RecruitmentSchedule)
admin.site.register(InterviewSchedule)
admin.site.register(Application)
admin.site.register(InterviewSlot)