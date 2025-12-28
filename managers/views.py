from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ApplicationPeriod, InterviewPeriod, InterviewSchedule
from .serializers import ApplicationPeriodSerializer, InterviewPeriodSerializer, InterviewScheduleSerializer
from utils.choices import PartChoices, MethodChoices

class ApplicationBaseView(APIView):
    def get_params(self, request):
        recruit_year = request.query_params.get('recruit_year')
        part = request.query_params.get('part')

        if not recruit_year or not part:
            return None, None, Response(
                {"message": "recruit_year와 part 쿼리 파라미터가 필요합니다.", "error": {"required": ["recruit_year", "part"]}},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            recruit_year = int(recruit_year)
        except ValueError:
            return None, None, Response(
                {"message": "recruit_year는 정수여야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_parts = [k for k, _ in PartChoices.choices]
        if part not in valid_parts:
            return None, None, Response(
                {"message": f"part는 다음 값 중 하나여야 합니다: {', '.join(valid_parts)}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return recruit_year, part, None

class ApplicationPeriodView(ApplicationBaseView):
    def get(self, request):
        recruit_year, part, error_response = self.get_params(request)
        if error_response:
            return error_response
        
        instance = ApplicationPeriod.objects.filter(recruit_year=recruit_year, part=part).first()
        if not instance:
            instance = ApplicationPeriod.objects.create(recruit_year=recruit_year, part=part)
        
        return Response(
            {"message": "지원서 모집 기간 조회 성공", "data": ApplicationPeriodSerializer(instance).data},
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        recruit_year, part, error_response = self.get_params(request)
        if error_response:
            return error_response
        
        if "start_datetime" not in request.data and "end_datetime" not in request.data:
            return Response(
                {"message": "수정할 값이 존재하지 않습니다.", "error": {"required_one_of": ["start_datetime", "end_datetime"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance, _ = ApplicationPeriod.objects.get_or_create(recruit_year=recruit_year, part=part)

        serializer = ApplicationPeriodSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": "지원서 모집 기간 수정 실패", "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            {"message": "지원서 모집 기간 수정 성공", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

class ApplicationPeriodStartView(ApplicationBaseView):
    def post(self, request):
        recruit_year, part, error_response = self.get_params(request)
        if error_response:
            return error_response
        
        instance, _ = ApplicationPeriod.objects.get_or_create(recruit_year=recruit_year, part=part)

        now = timezone.now()
        instance.start_datetime = now
        instance.save(update_fields=["start_datetime", "updated_at"])

        return Response(
            {"message": "지금 모집 시작 성공", "data": ApplicationPeriodSerializer(instance).data},
            status=status.HTTP_200_OK,
        )

class ApplicationPeriodEndView(ApplicationBaseView):
    def post(self, request):
        recruit_year, part, error_response = self.get_params(request)
        if error_response:
            return error_response
        
        instance, _ = ApplicationPeriod.objects.get_or_create(recruit_year=recruit_year, part=part)

        now = timezone.now()
        instance.end_datetime = now
        instance.save(update_fields=["end_datetime", "updated_at"])

        return Response(
            {"message": "지금 모집 마감 성공", "data": ApplicationPeriodSerializer(instance).data},
            status=status.HTTP_200_OK,
        )

class InterviewPeriodView(ApplicationBaseView):
    def get(self, request):
        recruit_year, part, error_response = self.get_params(request)
        if error_response:
            return error_response
        
        instance, _ = InterviewPeriod.objects.get_or_create(recruit_year=recruit_year, part=part)

        return Response(
            {"message": "면접 기간 조회 성공", "data": InterviewPeriodSerializer(instance).data},
            status=status.HTTP_200_OK,
        )
    
    def patch(self, request):
        recruit_year, part, error_response = self.get_params(request)
        if error_response:
            return error_response
        
        if "start_date" not in request.data and "end_date" not in request.data:
            return Response(
                {
                    "message": "수정할 값이 존재하지 않습니다.",
                    "error": {"required_one_of": ["start_date", "end_date"]},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance, _ = InterviewPeriod.objects.get_or_create(recruit_year=recruit_year, part=part)

        serializer = InterviewPeriodSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": "면접 기간 수정 실패", "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            {"message": "면접 기간 수정 성공", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

class InterviewBaseView(APIView):
    def get_params(self, request):
        recruit_year = request.query_params.get('recruit_year')
        part = request.query_params.get('part')
        method = request.query_params.get('method')

        if not recruit_year or not part or not method:
            return None, None, None, Response(
                {
                    "message": "recruit_year, part, method 쿼리 파라미터가 필요합니다.",
                    "error": {"required": ["recruit_year", "part", "method"]},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            recruit_year = int(recruit_year)
        except ValueError:
            return None, None, None, Response(
                {"message": "recruit_year는 정수여야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_parts = [k for k, _ in PartChoices.choices]
        if part not in valid_parts:
            return None, None, None, Response(
                {"message": f"part는 다음 값 중 하나여야 합니다: {', '.join(valid_parts)}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_methods = [k for k, _ in MethodChoices.choices]
        if method not in valid_methods:
            return None, None, None, Response(
                {"message": f"method는 다음 값 중 하나여야 합니다: {', '.join(valid_methods)}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return recruit_year, part, method, None

class InterviewScheduleView(InterviewBaseView):
    def get(self, request):
        recruit_year, part, method, error_response = self.get_params(request)
        if error_response:
            return error_response
        
        date_str = request.query_params.get('date')
        qs = InterviewSchedule.objects.filter(recruit_year=recruit_year, part=part, method=method).order_by('date')

        if date_str:
            instance = qs.filter(date=date_str).first()
            return Response(
                {
                    "message": "면접 일정 조회 성공",
                    "data": InterviewScheduleSerializer(instance).data if instance else None,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "면접 일정 목록 조회 성공", "data": InterviewScheduleSerializer(qs, many=True).data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        recruit_year, part, method, error_response = self.get_params(request)
        if error_response:
            return error_response

        if "date" not in request.data or "slots_gui" not in request.data:
            return Response(
                {"message": "date와 slots_gui는 필수입니다.", "error": {"required": ["date", "slots_gui"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = InterviewScheduleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "면접 일정 등록 실패", "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        target_date = serializer.validated_data["date"]
        conflict = InterviewSchedule.objects.filter(
            recruit_year=recruit_year,
            part=part,
            date=target_date,
        ).exclude(method=method).exists()

        if conflict:
            return Response(
                {
                    "message": "면접 일정 등록 실패",
                    "error": {"date_conflict": "대면/비대면 면접은 서로 다른 날짜로 설정해 주세요."},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = InterviewSchedule.objects.create(
            recruit_year=recruit_year,
            part=part,
            method=method,
            date=serializer.validated_data["date"],
            slots=serializer.validated_data.get("slots_raw", []),
        )

        return Response(
            {"message": "면접 일정 등록 성공", "data": InterviewScheduleSerializer(instance).data},
            status=status.HTTP_201_CREATED,
        )

class InterviewScheduleDetailView(APIView):
    def patch(self, request, pk: int):
        instance = InterviewSchedule.objects.filter(pk=pk).first()
        if not instance:
            return Response(
                {"message": "면접 일정을 찾을 수 없어요.", "error": {"not_found": pk}},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        if "date" not in request.data and "slots_gui" not in request.data:
            return Response(
                {"message": "수정할 값이 존재하지 않습니다.", "error": {"required_one_of": ["date", "slots_gui"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_date = request.data.get("date", None)
        if new_date is not None:
            conflict = InterviewSchedule.objects.filter(
                recruit_year=instance.recruit_year,
                part=instance.part,
                date=new_date,
            ).exclude(method=instance.method).exclude(pk=instance.pk).exists()

            if conflict:
                return Response(
                    {
                        "message": "면접 일정 수정 실패",
                        "error": {"date_conflict": "대면/비대면 면접은 서로 다른 날짜로 설정해 주세요."},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = InterviewScheduleSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": "면접 일정 수정 실패", "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(
            {"message": "면접 일정 수정 성공", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk: int):
        instance = InterviewSchedule.objects.filter(pk=pk).first()
        if not instance:
            return Response(
                {"message": "면접 일정을 찾을 수 없어요.", "error": {"not_found": pk}},
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.delete()
        return Response(
            {"message": "면접 일정 삭제 성공", "data": {"deleted_id": pk}},
            status=status.HTTP_200_OK,
        )