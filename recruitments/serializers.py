from rest_framework import serializers
from .models import Application

class ApplicationDetailSerializer(serializers.Serializer):
    """
    지원서 추가, 지원서 상세 조회 API에서 사용합니다.
    """
    class Meta:
        model = Application
        fields  =   (
                        "name","phone_number","birthday","department","student_number","grade",
                        "interview_method","interview_available_times",
                        "part","personal_statement_1","personal_statement_2","personal_statement_3","personal_statement_4","personal_statement_5",
                        "completed_prerequisites","portfolios",
                        "application_code",
                    )
        extra_kwargs = {"application_code": {"write_only": True}}
