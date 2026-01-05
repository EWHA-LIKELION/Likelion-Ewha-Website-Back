from rest_framework import serializers
from .models import *
from utils.choices import InterviewMethodChoices

class InterviewDateSerializer(serializers.Serializer):
    part = serializers.CharField()
    dates = serializers.ListField(
        child = serializers.CharField()
    )

class InterviewSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSlot
        fields = [
            "id",
            "start",
            "end",
            "max_capacity",
            "assigned_count",
        ]
    
    def get_assigned_count(self, slot):
        return Application.objects.filter(
            interview_at=slot.start,
            part=slot.interview_schedule.part,
        ).count()

class InterviewApplicantSerializer(serializers.ModelSerializer):
    available_slot_count = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            "name",
            "student_number",
            "available_slot_count",
            "interview_method",
            "interview_at",
        ]

    def get_available_slot_count(self, obj):
        return len(obj.interview_available_times)

class ApplicantSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSlot
        fields = [
            "id",
            "start",
            "end",
        ]

class SlotAssignSerializer(serializers.Serializer):
    student_number = serializers.CharField(max_length=7)
    slot_id = serializers.IntegerField()

    def validate(self, data):
        student_number = data["student_number"]
        slot_id = data["slot_id"]

        try:
            application = Application.objects.get(
                student_number=student_number
            )
        except Application.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 지원자입니다.")
        
        try:
            slot = InterviewSlot.objects.get(id=slot_id)
        except InterviewSlot.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 슬롯입니다.")
        
        data["application"] = application
        data["slot"] = slot
        return data
    
class AssignedApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "student_number",
            "name",
        ]

class AssignedSlotSerializer(serializers.ModelSerializer):
    assigned_applicants = serializers.SerializerMethodField()

    class Meta:
        model = InterviewSlot
        fields = [
            "id",
            "start",
            "end",
            "assigned_applicants",
        ]
    
    def get_assigned_applicants(self, slot):
        """
        해당 슬롯 시간(start)에 배정된 지원자 목록
        """
        applications = Application.objects.filter(
            interview_at=slot.start
        )

        return AssignedApplicantSerializer(applications, many=True).data
    
