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
    FRONTEND  = 'FRONTEND',  '프론트엔드'
    BACKEND   = 'BACKEND',   '백엔드'

class InterviewMethodChoices(TextChoices):
    OFFLINE = 'OFFLINE', '대면'
    ONLINE  = 'ONLINE',  '비대면'

class StatusChoices(TextChoices):
    FIRST_PENDING  = 'FIRST_PENDING',  '1차 심사중'
    FIRST_ACCEPTED = 'FIRST_ACCEPTED', '1차 합격'
    FIRST_REJECTED = 'FIRST_REJECTED', '1차 불합격'
    FINAL_ACCEPTED = 'FINAL_ACCEPTED', '최종 합격'
    FINAL_REJECTED = 'FINAL_REJECTED', '최종 불합격'
