from django.contrib import admin
from .models import RecruitmentYear, RecruitmentSchedule, InterviewSchedule, Application

admin.site.register(RecruitmentYear)
admin.site.register(RecruitmentSchedule)
admin.site.register(InterviewSchedule)
admin.site.register(Application)
