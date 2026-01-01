from django.http import HttpRequest
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CombinedScheduleSerializer
from .services import RecruitmentScheduleService

class CombinedScheduleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request:HttpRequest, format=None):
        year = request.query_params.get('year')
        if not year:
            return Response(
                {"message": "year 쿼리 파라미터가 필요합니다.", "error": {"required": ["year"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        service = RecruitmentScheduleService(request, year=int(year))
        data = service.get()
        return Response(
            {"message": "모집 일정 조회 성공", "data": data},
            status=status.HTTP_200_OK,
        )

    def patch(self, request:HttpRequest, format=None):
        year = request.query_params.get('year')
        if not year:
            return Response(
                {"message": "year 쿼리 파라미터가 필요합니다.", "error": {"required": ["year"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CombinedScheduleSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": "요청 값이 올바르지 않습니다.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = RecruitmentScheduleService(request, year=int(year))
        try:
            data = service.patch(validated_data=serializer.validated_data)
            return Response(
                {"message": "모집 일정 수정 성공", "data": data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "모집 일정 수정 실패", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )