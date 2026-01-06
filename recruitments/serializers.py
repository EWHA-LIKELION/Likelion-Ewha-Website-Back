from datetime import datetime
import re
from string import ascii_uppercase, digits
from django.core.validators import FileExtensionValidator
from rest_framework import serializers
import nanoid
from utils.choices import InterviewMethodChoices, PartChoices
from utils.validators import FileSizeValidator
from .models import InterviewSchedule, Application

class ApplicationCreateSerializer(serializers.Serializer):
    """
    지원서 추가 API용 시리얼라이저
    """
    interview_method = serializers.ChoiceField(choices=InterviewMethodChoices.choices)
    interview_available_times = serializers.ListField(child=serializers.DateTimeField(), min_length=1)
    part = serializers.ChoiceField(choices=PartChoices.choices)
    completed_prerequisites = serializers.ListField(
        child=serializers.ImageField(
            validators=[
                FileExtensionValidator(allowed_extensions=["png","jpg","jpeg","gif"]),
                FileSizeValidator(min_size_MB=0, max_size_MB=20),
            ],
        ),
        max_length=3,
        required=False,
        allow_null=True,
    )
    portfolios = serializers.ListField(
        child=serializers.FileField(
            validators=[
                FileExtensionValidator(allowed_extensions=["png","jpg","jpeg","gif","pdf"]),
                FileSizeValidator(min_size_MB=0, max_size_MB=100),
            ],
        ),
        max_length=3,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Application
        fields = (
                    "name","phone_number","birthday","department","student_number","grade",
                    "interview_method","interview_available_times",
                    "part","personal_statement_1","personal_statement_2","personal_statement_3","personal_statement_4","personal_statement_5",
                    "completed_prerequisites","portfolios",
                 )

    def validate_phone_number(self, value:str):
        phone_regex = r"^01([0|1|6|7|8|9])-?([0-9]{4})-?([0-9]{4})$"

        if not re.match(phone_regex, value):
            raise serializers.ValidationError(detail="전화번호를 '010-0000-0000' 형식으로 입력해 주세요.")

        return value

    def validate_interview_available_times(self, value:list[datetime]):
        if len(value) != len(set(value)):
            raise serializers.ValidationError(detail="면접 일정은 중복으로 선택할 수 없습니다.")

        interview_schedules:list[InterviewSchedule] = self.context.get("interview_schedules", list())
        if not interview_schedules:
            raise serializers.ValidationError(detail="면접 일정이 준비되지 않았습니다.")

        for interview_available_time in value:
            is_valid = any(
                interview_schedule.start <= interview_available_time <= interview_schedule.end
                for interview_schedule in interview_schedules
            )
            # 30분 단위의 선택지를 선택했는지 확인하기
            if not is_valid:
                raise serializers.ValidationError(detail=f"면접 일정 '{interview_available_time}'은/는 선택할 수 없습니다.")

        return sorted(value)

    # def validate_completed_prerequisites(self, value:list):
    #     ALLOWED_MIME_TYPES = {"image/png","image/jpg","image/jpeg","image/gif"}
    #
    #     for file_obj in value:
    #         # 포맷 검증
    #             # python-magic 라이브러리(의존하는 libmagic 라이브러리를 Docker나 배포 환경에 설치해야 함)
    #             # read(2048)로 앞부분만 읽어서 판단하므로 매우 빠름
    #         # 이미지 재저장
    #             # 이미지의 메타데이터를 날리고 순수 픽셀 데이터만 남김
    #             # 이미지를 다시 저장하거나 포맷을 변환하면, 이미지 안에 숨겨진 악성 스크립트를 제거할 수 있음
    #     return value

    # def validate_portfolios(self, value:list):
    #     ALLOWED_MIME_TYPES = {"image/png","image/jpg","image/jpeg","image/gif","application/pdf"}
    #
    #     for file_obj in value:
    #         # 포맷 검증
    #             # 위와 동일
    #         # 내용 정밀 검증
    #             # PDF 비암호화 여부: 암호화된 PDF는 업로드할 수 없음
    #             # 페이지 1장 이상: 빈 파일은 업로드할 수 없음
    #             # 파일 끝부분이 잘리지 않았는지 확인 (마지막 페이지 데이터 접근)
    #     return value

    def create(self, validated_data:dict)->str:
        completed_prerequisites:list = validated_data.pop("completed_prerequisites")
        portfolios:list = validated_data.pop("portfolios")

        # 지원 코드 생성
        application_code = nanoid.generate(alphabet=ascii_uppercase+digits, size=10)

        # 지원 코드 단방향 암호화
        # 나머지 정보(이미지, 포트폴리오 제외) 양방향 암호화

        # 데이터베이스 저장
        Application.objects.create(
            application_code=application_code,
            completed_prerequisite_1=completed_prerequisites[0],
            completed_prerequisite_2=completed_prerequisites[1],
            completed_prerequisite_3=completed_prerequisites[2],
            portfolio_1=portfolios[0],
            portfolio_2=portfolios[1],
            portfolio_3=portfolios[2],
            **validated_data,
        )

        return application_code
