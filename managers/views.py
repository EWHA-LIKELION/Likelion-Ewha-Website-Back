from django.db.models import Q, Case, When, IntegerField
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from applications.models import Application
from .serializers import ApplicationSerializer, ApplicationUpdateSerializer
from utils.choices import PartChoices

class ApplicationListView(APIView):
    permission_classes = [AllowAny] #로그인 로직 추가 이후 접근 권한 설정 필요(IsAuthenticated)

    def get(self, request):
        # 필터링
        filters = Q()

        part = request.query_params.get("part")
        status = request.query_params.get("status")
        interview_method = request.query_params.get("interview_method")

        if part:
            filters &= Q(part=part)
        if status:
            filters &= Q(status=status)
        if interview_method:
            filters &= Q(interview_method=interview_method)
            
        # 검색
        search = request.query_params.get("search")
        if search:
            keywords = [k.strip() for k in search.split(",") if k.strip()] # ,로 다중 검색

            for keyword in keywords:
                filters &= (
                    Q(name__icontains=keyword) | 
                    Q(phone_number__icontains=keyword) | 
                    Q(application_code__icontains=keyword)
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
        
        return Response(data)

class ApplicationDetailView(APIView):
    permission_classes = [AllowAny] #로그인 로직 추가 이후 접근 권한 설정 필요(IsAuthenticated)

    def get(self, request, student_number): #get 함수
        application = get_object_or_404(Application, student_number=student_number)

        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=200)

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