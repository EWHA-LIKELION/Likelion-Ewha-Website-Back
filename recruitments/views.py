from django.http import HttpRequest
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RecruitmentYear, RecruitmentSchedule, InterviewSchedule
from .serializers import ApplicationCreateSerializer

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

        # 요청값 검증
        interview_schedules = list(
            InterviewSchedule.objects
            .filter(recruitment_schedule__year=current_time.year)
            .order_by("start")
        )
        serializer = ApplicationCreateSerializer(
            data=request.data,
            context={"interview_schedules": interview_schedules}
        )
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        application_code = serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data={"application_code":application_code},
        )

class RecruitmentYearView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        current_year = timezone.now().year
        RecruitmentYear.objects.get_or_create(year=current_year)

        years = list(
            RecruitmentYear.objects
            .order_by("-year")
            .values_list("year", flat=True) #연도값만 받기 때문에 리스트로 변환
        )

        return Response(
            {"years":years}, 
            status=status.HTTP_200_OK,
            )
