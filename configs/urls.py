from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)

urlpatterns = [
    path('', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('managers/', include('managers.urls')),
    path('accounts/', include('accounts.urls')),
    path('recruitments/', include('recruitments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
