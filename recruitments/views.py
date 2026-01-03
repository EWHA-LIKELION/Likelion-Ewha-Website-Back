from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import RecruitmentSchedule

class RecruitmentYearListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        schedules = RecruitmentSchedule.objects.order_by("-year")
        years = [s.year for s in schedules]

        return Response({"years": years})