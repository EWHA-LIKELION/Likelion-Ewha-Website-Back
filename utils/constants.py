from enum import Enum

class Example(Enum):
    """
    예시 코드입니다.
    """
    example = 'example:{value}'

    def format(self, **kwargs):
        return self.value.format(**kwargs)

class CacheKey(Enum):
    SET_APPLICATION_FIRST_PENDING = 'application:first_pending'
    SET_APPLICATION_FIRST_ACCEPTED = 'application:first_accepted'

    def format(self, **kwargs):
        return self.value.format(**kwargs)
