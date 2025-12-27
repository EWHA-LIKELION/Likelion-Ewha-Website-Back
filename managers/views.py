from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ApplicationPeriod
from .serializers import ApplicationPeriodSerializer
from utils.choices import PartChoices

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