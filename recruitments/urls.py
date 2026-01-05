from django.urls import path
from .views import *

app_name = 'recruitments'

urlpatterns = [
    path('interview-group/dates/', InterviewDateListView.as_view()), #면접 날짜 조회 
    path('interview-group/slots/', InterviewSlotListView.as_view()), #슬롯 생성 및 조회 
    path('interview-group/applicants/', InterviewApplicantListView.as_view()), #면접 대상자 정보 조회 
    path('interview-group/<str:student_number>/avail-slots/', AvailableSlotListView.as_view()), #지원자별 면접 가능 슬롯 조회 
    path('interview-group/assign-slot/', AssignSlotView.as_view()), #슬롯 배정 
    path('interview-group/cancel-slot/', CancelSlotView.as_view()), #슬롯 배정 취소 
    path('interview-group/assigned-slots/', AssignedSlotListView.as_view()) #슬롯별 배정 인원 전체 조회 
]
