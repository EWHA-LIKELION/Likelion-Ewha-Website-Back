from django.contrib import admin
from .models import Manager, AllowedManagerEmail, RecruitmentSchedule, InterviewSchedule

admin.site.register(Manager)
admin.site.register(AllowedManagerEmail)
admin.site.register(RecruitmentSchedule)
admin.site.register(InterviewSchedule)
