from components.general.caching.cache import cache_method
from rest_framework.viewsets import ModelViewSet


class CacheModelViewSet(ModelViewSet):
    """Provides default cache realisation for `retrieve` and `list` methods

    Class provides cache realisation for `retrieve` and `list` methods
    by using custom `cache_method` which is created to cache viewset methods.

    To use this class just create attributes in ViewSet called `cache_key` and `timeout`
    and specify values for them.

    Base args:
        default_cache_key: ''
        default_timeout: 25
    """
    default_cache_key = ''
    default_timeout = 25

    def retrieve(self, request, *args, **kwargs):
        cache_key = getattr(
            self,
            'cache_key',
            self.default_cache_key
        ) + '_retrieve'
        timeout = getattr(self, 'timeout', self.default_timeout)

        return self.cached_method_wrapper(super().retrieve, cache_key=cache_key, timeout=timeout)(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        cache_key = getattr(
            self,
            'cache_key',
            self.default_cache_key
        ) + '_list'
        timeout = getattr(self, 'timeout', self.default_timeout)

        return self.cached_method_wrapper(super().list, cache_key=cache_key, timeout=timeout)(request, *args, **kwargs)

    def cached_method_wrapper(self, func, cache_key, timeout):
        return cache_method(cache_key=cache_key, timeout=timeout)(func)
