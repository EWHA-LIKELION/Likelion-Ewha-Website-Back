from django.http import HttpRequest
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import ApplicationService

class ApplicationView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def post(self, request:HttpRequest, format=None):
        # 서류 접수 기간인지 확인
        # 시리얼라이저 통해 요청값 검증

        application_service = ApplicationService(request)
        application = application_service.post()

        return Response(
            status=status.HTTP_201_CREATED,
            data={"application_code":지원코드},
        )
