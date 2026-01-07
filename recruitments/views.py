from django.db.models import Q, Case, When, IntegerField
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Application, RecruitmentSchedule
from .serializers import ApplicationSerializer
from utils.choices import PartChoices

class ApplicationListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

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
            try:
                schedule = RecruitmentSchedule.objects.get(year=year)
                filters &= Q(
                    created_at__gte = schedule.application_start,
                    created_at__lte = schedule.application_end,
                )
            except RecruitmentSchedule.DoesNotExist:
                return Response(
                    {"detail": "해당 모집 연도가 존재하지 않습니다"},
                    status=400
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
                    Q(phone_number__icontains=keyword) | 
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
                "application_code",
            )
        else:
            applications = applications.order_by(
                "part_order",
                "name",
                "application_code",
            )

        serializer = ApplicationSerializer(applications, many=True)
        data = serializer.data
        
        for idx, item in enumerate(data, start=1):
            item["order"] = idx
        
        return Response({
            "filter_counts": filter_counts,
            "results": data, 
        })