from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Application
from .serializers import ApplicantSerializer

class ApplicantDetailView(APIView):
    permission_classes = [AllowAny] #로그인 로직 추가 이후 접근 권한 설정 필요

    def get(self, request, application_id): #id 확인용 임시 get 함수
        application = get_object_or_404(Application, id=application_id)

        serializer = ApplicantSerializer(application)
        return Response(serializer.data, status=200)

    def delete(self, request, application_id):
        application = get_object_or_404(Application, id=application_id)
        application.delete()
        return Response({"detail":"지원자 정보가 삭제되었습니다."},status=status.HTTP_200_OK,)