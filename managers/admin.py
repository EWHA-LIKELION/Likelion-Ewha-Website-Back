from django.contrib import admin
from .models import ApplicationPeriod, InterviewPeriod, InterviewSchedule

admin.site.register(ApplicationPeriod)
admin.site.register(InterviewPeriod)
admin.site.register(InterviewSchedule)