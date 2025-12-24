import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.dev")  # 너 프로젝트에 맞게 경로 조정 필요
django.setup()

print("DATABASE_URL env:", repr(os.getenv("DATABASE_URL")))
print("Django DATABASES:", settings.DATABASES)
