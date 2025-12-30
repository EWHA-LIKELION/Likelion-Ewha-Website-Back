from django.http import HttpRequest

class ApplicationService:
    def __init__(self, request:HttpRequest):
        self.request = request

    def post(self):
        pass
        # 첨부파일 S3 업로드 및 URL 생성
        # 지원 코드 생성
        # 지원 코드 단방향 암호화
        # 나머지 정보 양방향 암호화
        # 시리얼라이저 통해 요청값 검증 및 데이터베이스 저장
