from django.contrib import admin
from .models import User, RecruitmentSchedule, InterviewSchedule

admin.site.register(User)
admin.site.register(RecruitmentSchedule)
admin.site.register(InterviewSchedule)
