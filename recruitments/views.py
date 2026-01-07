from django.http import HttpRequest
from django.utils import timezone
from django.db.models import Q, Case, When, IntegerField
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Application, RecruitmentSchedule, InterviewSchedule
from .serializers import ApplicationCreateSerializer, ApplicationListSerializer
from utils.choices import PartChoices

class ApplicationView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        else:
            return [IsAuthenticated(), IsAdminUser()]

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

    def get(self, request):
        # 필터링
        filters = Q()

        part = request.query_params.getlist("part")
        status = request.query_params.getlist("status")
        interview_method = request.query_params.getlist("interview_method")
        year = request.query_params.get("year") #다중필터링이 아니라서 getlist가 아닌 get

        if part:
            filters &= Q(part__in=part)
        if status:
            filters &= Q(status__in=status)
        if interview_method:
            filters &= Q(interview_method__in=interview_method)

        if year:
            schedule = RecruitmentSchedule.objects.get(year=year)
            filters &= Q(
                created_at__gte = schedule.application_start,
                created_at__lte = schedule.application_end,
            )

        filter_counts = {
            "part" : len(part),
            "status" : len(status),
            "interview_method" : len(interview_method),
        }
            
        # 검색
        search = request.query_params.get("search")
        if search:
            keywords = [k.strip() for k in search.split(",") if k.strip()] # ,로 다중 검색

            for keyword in keywords:
                filters &= (
                    Q(name__icontains=keyword) | 
                    Q(student_number__icontains=keyword) |
                    Q(phone_number__icontains=keyword)
                )
        applications = Application.objects.filter(filters)

        # 파트 정렬 기준 정의 (기디 -> 프론트 -> 백)
        part_order = Case(
            When(part=PartChoices.PM_DESIGN, then=0),
            When(part=PartChoices.FRONTEND, then=1),
            When(part=PartChoices.BACKEND, then=2),
            output_field=IntegerField(),
        )

        applications = applications.annotate(part_order=part_order)

        # 정렬 (기본순, 면접순)
        order = request.query_params.get("order", "default")

        if order == "interview":
            applications = applications.order_by(
                "part_order",
                "interview_at",
            )
        else:
            applications = applications.order_by(
                "part_order",
                "name",
            )

        serializer = ApplicationListSerializer(applications, many=True)
        data = serializer.data
        
        for idx, item in enumerate(data, start=1):
            item["order"] = idx
        
        return Response({
            "filter_counts": filter_counts,
            "results": data, 
        })
