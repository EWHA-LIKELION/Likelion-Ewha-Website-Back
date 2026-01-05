from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from recruitments.models import RecruitmentSchedule, InterviewSchedule
from recruitments.services import InterviewScheduleService


class InterviewGroupView(APIView):
    """
    GET /recuitments/application/interview-group/?part=BACKEND&interview_method=ONLINE
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        service = InterviewScheduleService(
            request=request
        )

        try:
            data = service.get_interview_group_options()
        except ValueError as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except RecruitmentSchedule.DoesNotExist:
            return Response(
                {"message": "Recruitment schedule not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except InterviewSchedule.DoesNotExist:
            return Response(
                {"message": "Interview schedules not found for given conditions."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            data,
            status=status.HTTP_200_OK
        )
