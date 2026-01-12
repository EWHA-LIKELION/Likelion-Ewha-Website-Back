from django.http import HttpRequest
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Application, RecruitmentSchedule, InterviewSchedule
from .serializers import ApplicationCreateSerializer, ApplicationUpdateSerializer

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

class ApplicationByStudentNumberView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, student_number):
        application = get_object_or_404(Application, student_number=student_number)
        application.delete()
        return Response({"detail":"지원자 정보가 삭제되었습니다."},status=status.HTTP_200_OK,)
    
    def patch(self, request, student_number):
        application = get_object_or_404(Application, student_number = student_number)

        serializer = ApplicationUpdateSerializer(
            application,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"수정이 완료되었습니다."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)