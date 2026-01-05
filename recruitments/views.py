from django.http import HttpRequest
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RecruitmentSchedule
from .services import ApplicationService

class ApplicationView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def post(self, request:HttpRequest, format=None):
        # 서류 접수 기간 검증
        current_time = timezone.now()
        try:
            recruitment_schedule = RecruitmentSchedule.objects.get(year=current_time.year)
        except:
            raise APIException(detail="모집 일정이 준비되지 않았습니다.")

        if not recruitment_schedule.application_start <= current_time <= recruitment_schedule.application_end:
            raise PermissionDenied(detail="서류 접수 기간이 아닙니다.")

        # 시리얼라이저 통해 요청값 검증

        application_service = ApplicationService(request)
        application = application_service.post()

        return Response(
            status=status.HTTP_201_CREATED,
            data={"application_code":지원코드},
        )
