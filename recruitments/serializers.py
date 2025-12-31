from rest_framework import serializers
from .models import Application

class ApplicationCreateSerializer(serializers.Serializer):
    """
    지원서 추가 API에서 사용합니다.
    """
    completed_prerequisites = 파일인지 검증
    portfolios = 파일

    class Meta:
        model = Application
        fields  =   (
                        "name","phone_number","birthday","department","student_number","grade",
                        "interview_method","interview_available_times",
                        "part","personal_statement_1","personal_statement_2","personal_statement_3","personal_statement_4","personal_statement_5",
                        "completed_prerequisites","portfolios",
                    )
    
    # 파일 개수 검증
        # 각 3개씩
    # 파일 확장자 검증
        # 선수강 확장자 png, jpg, jpeg, gif만 가능
        # 포트폴리오 png, jpg, jpeg, gif, pdf만 가능
    # 파일 용량 검증
        # 선수강 1파일당 20MB
        # 포트폴리오 1파일당 100MB
