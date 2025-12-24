from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import views
from rest_framework.response import Response
from .serializers import ManagerSerializer
# Create your views here.

class SignUpView(views.APIView):
    def post(self, request):
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공", "data": serializer.data})
        return Response({"message": "회원가입 실패", "errors": serializer.errors}, status=400)