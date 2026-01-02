from django.core.cache import cache
from .constants import CacheKey

class AbstractCache:
    def __init__(self, key):
        self.key = key

    def set(self, value, timeout:int|None=None, version:int|None=None):
        cache.set(self.key, value, timeout, version)

    def get(self, default=None, version:int|None=None):
        return cache.get(self.key, default, version)

class AbstractRedisSet:
    def __init__(self, key):
        self.key = key

    def add(self, value):
        cache.sadd(self.key, value)

    def remove(self, value):
        cache.srem(self.key, value)

    def count(self)->int:
        return cache.scard(self.key)

    def contains(self, value)->bool:
        return bool(cache.sismember(self.key, value))
