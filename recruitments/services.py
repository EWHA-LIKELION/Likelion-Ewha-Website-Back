from django.http import HttpRequest

class ApplicationService:
    def __init__(self, request:HttpRequest):
        self.request = request

    def post(self):
        pass
