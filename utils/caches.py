from django.core.cache import cache

class AbstractCache:
    def __init__(self, key):
        self.key = key

    def set(self, value, timeout:int|None=None, version:int|None=None):
        cache.set(
            key=self.key,
            value=value,
            timeout=timeout,
            version=version,
        )

    def get(self, default=None, version:int|None=None):
        return cache.get(
            key=self.key,
            default=default,
            version=version,
        )
