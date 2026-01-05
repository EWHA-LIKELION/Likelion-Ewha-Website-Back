from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from utils.generate_slots import generate_slots

# Create your views here.

# 파트별 면접 날짜 조회 
class InterviewDateListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        part = request.query_params.get("part")

        if not part:
            return Response(
                {"detail": "part 입력이 필요합니다."},
                status = status.HTTP_400_BAD_REQUEST,
            )
        
        schedules = InterviewSchedule.objects.filter(part=part)

        dates = sorted({
            schedule.start.date()
            for schedule in schedules
        })

        serializer = InterviewDateSerializer({
            "part": part,
            "dates": dates
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 슬롯 조회 
class InterviewSlotListView(APIView):
    def get(self, request):
        year = request.query_params["year"]
        part = request.query_params["part"]

        schedule = InterviewSchedule.objects.get(
            recruitment_schedule__year=year,
            part=part,
        )

        # 슬롯이 아직 없으면 자동 생성
        if not schedule.slots.exists():
            generate_slots(schedule)

        slots = schedule.slots.all()
        return Response(InterviewSlotSerializer(slots, many=True).data)

# 면접대상자 정보 조회 
class InterviewApplicantListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        year = request.query_params.get("year")
        part = request.query_params.get("part")

        qs = Application.objects.filter(
            part=part,
            created_at__year=year,
        )

        serializer = InterviewApplicantSerializer(qs, many=True)
        return Response(serializer.data)
    
# 선택 가능한 면접 슬롯 목록 조회 
class AvailableSlotListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, student_number):
        year = request.query_params.get("year")
        part = request.query_params.get("part")

        #지원자 조회
        application = get_object_or_404(
            Application,
            student_number=student_number,
            part=part,
        )

        #면접 일정 조회
        schedule = get_object_or_404(
            InterviewSchedule,
            recruitment_schedule__year=year,
            part=part,
        )

        #슬롯 조회
        slots = InterviewSlot.objects.filter(
            interview_schedule=schedule,
            start__in=application.interview_available_times,
        )

        serializer = ApplicantSlotSerializer(slots, many=True)
        return Response(serializer.data)

# 면접 슬롯 배정 
class AssignSlotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        student_number = request.data.get("student_number")
        slot_id = request.data.get("slot_id")

        # 지원자 조회
        application = get_object_or_404(
            Application,
            student_number=student_number,
        )
     
        # 이미 배정된 지원자인 경우
        if application.interview_at is not None:
            return Response(
                {"detail": "이미 면접 슬롯이 배정된 지원자입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        #슬롯 조회
        slot = get_object_or_404(
            InterviewSlot,
            id=slot_id,
        )

        # 지원자 가능 슬롯 제한
        if slot.start not in application.interview_available_times:
            return Response(
                {"detail": "지원자가 선택한 면접 가능 시간에 포함되지 않은 슬롯입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        # 슬롯 정원 체크
        assigned_count = Application.objects.filter(
            interview_at=slot.start,
        ).count()

        # 슬롯 정원 초과일 경우
        if assigned_count >= slot.max_capacity:
            return Response(
                {"detail": "해당 슬롯의 정원이 초과되었습니다."},
                status=status.HTTP_409_CONFLICT,
            )
            
        # 배정
        application.interview_at = slot.start
        application.save(update_fields=["interview_at"])

        return Response(
            {
                "message": "면접 슬롯이 배정되었습니다.",
                "student_number": application.student_number,
                "slot_id": slot.id,
            },
            status=status.HTTP_201_CREATED,
        )

# 면접 배정 취소 
class CancelSlotView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request):
        serializer = SlotAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        application = serializer.validated_data["application"]
        slot = serializer.validated_data["slot"]

        application.interview_at = None
        application.save(update_fields=["interview_at"])

        return Response(
            {
                "message": "슬롯 배정 취소 완료",
                "student_number": application.student_number,
                "slot_id": slot.id,
            },
            status=status.HTTP_200_OK,
        )

# 배정된 지원자 조회
class AssignedSlotListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        year = request.query_params.get("year")
        part = request.query_params.get("part")

        if not year or not part:
            return Response(
                {"detail": "year와 part는 필수입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 면접 일정 조회
        schedule = get_object_or_404(
            InterviewSchedule,
            recruitment_schedule__year=year,
            part=part,
        )

        # 해당 일정의 모든 슬롯
        slots = InterviewSlot.objects.filter(
            interview_schedule=schedule
        ).order_by("start")

        serializer = AssignedSlotSerializer(slots, many=True)
        return Response(serializer.data)
    
