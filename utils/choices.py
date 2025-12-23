from django.db.models import TextChoices, IntegerChoices

class ExampleChoices(IntegerChoices):
    """
    예시 코드입니다.
    """
    ONE   = 1, "일"
    TWO   = 2, "이"
    THREE = 3, "삼"

class PartChoices(TextChoices):
    PM_DESIGN = 'PM_DESIGN', '기획·디자인'
    FRONTEND  = 'FRONTEND', '프론트엔드'
    BACKEND   = 'BACKEND', '백엔드'

class MethodChoices(TextChoices):
    OFFLINE = 'OFFLINE', '대면'
    ONLINE = 'ONLINE', '비대면'