from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Application
from .serializers import ApplicationUpdateSerializer

class ApplicationDetailView(APIView):
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