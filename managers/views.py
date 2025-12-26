from rest_framework.views import APIView
from rest_framework.response import Response

class AlwaysOkView(APIView):
    def get(self, request):
        return Response({"message": "GET 요청 성공"}, status=200)