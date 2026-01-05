from __future__ import annotations
from rest_framework import serializers

# 날짜별 면접 슬롯(오전/오후) 응답 Serializer
class InterviewGroupDateSerializer(serializers.Serializer):
    date = serializers.CharField()
    am = serializers.ListField(
        child=serializers.CharField()
    )
    pm = serializers.ListField(
        child=serializers.CharField()
    )

# 면접 선택지(날짜별/오전·오후) 응답 Serializer
class InterviewGroupResponseSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    part = serializers.CharField()
    interview_method = serializers.CharField()
    dates = InterviewGroupDateSerializer(
        many=True
    )

