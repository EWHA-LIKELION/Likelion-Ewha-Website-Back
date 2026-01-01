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

class AbstractRedisSet:
    def __init__(self, key):
        self.key = key

    def add(self, value):
        cache.sadd(
            key=self.key,
            value=value,
        )

    def remove(self, value):
        cache.srem(
            key=self.key,
            value=value,
        )

    def count(self)->int:
        return cache.scard(key=self.key)

    def contains(self, value)->bool:
        return bool(
            cache.sismember(
                key=self.key,
                value=value,
            )
        )
