from django.contrib import admin
from .models import RecruitmentSchedule, InterviewSchedule, Application

admin.site.register(RecruitmentSchedule)
admin.site.register(InterviewSchedule)
admin.site.register(Application)
