from django.http import HttpRequest
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RecruitmentSchedule, InterviewSchedule
from .serializers import ApplicationCreateSerializer, CombinedScheduleSerializer
from .services import RecruitmentScheduleService

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

class RecruitmentScheduleView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get(self, request:HttpRequest, format=None):
        year = request.query_params.get('year')
        if not year:
            return Response(
                {"datail": "year 쿼리 파라미터가 필요합니다.", "error": {"required": ["year"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        only = request.query_params.get("only")

        service = RecruitmentScheduleService(request, year=int(year))
        data = service.get()

        if only == "recruitment":
            return Response(
                {"recruitment_schedule": data.get("recruitment_schedule")},
                status=status.HTTP_200_OK,
            )
        
        return Response(
            data,
            status=status.HTTP_200_OK,
        )
    
    def post(self, request:HttpRequest, format=None):
        year = request.query_params.get('year')
        if not year:
            return Response(
                {"detail": "year 쿼리 파라미터가 필요합니다.", "error": {"required": ["year"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer = CombinedScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = RecruitmentScheduleService(request)
        data = service.post(year=int(year), validated_data=serializer.validated_data)

        return Response(
            data,
            status=status.HTTP_201_CREATED,
        )
    
    def patch(self, request:HttpRequest, format=None):
        year = request.query_params.get('year')
        if not year:
            return Response(
                {"detail": "year 쿼리 파라미터가 필요합니다.", "error": {"required": ["year"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CombinedScheduleSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        service = RecruitmentScheduleService(request, year=int(year))
        data = service.patch(validated_data=serializer.validated_data)
        
        return Response(
            data,
            status=status.HTTP_200_OK,
        )