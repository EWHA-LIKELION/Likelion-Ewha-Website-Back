from django.contrib import admin
from .models import ApplicationPeriod, InterviewPeriod, Manager, AllowedManagerEmail

admin.site.register(ApplicationPeriod)
admin.site.register(InterviewPeriod)
admin.site.register(Manager)
admin.site.register(AllowedManagerEmail)