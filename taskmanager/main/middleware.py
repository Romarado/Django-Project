from django.utils.deprecation import MiddlewareMixin

import threading
_local_storage = threading.local()


class CurrentRequestMiddlewareMixin(MiddlewareMixin):
    def process_request(self, request):
        _local_storage.request = request


def get_current_request():
    return getattr(_local_storage, 'request', None)


def get_current_user():
    request = get_current_request()
    return getattr(request, 'user', None) if request is not None else None
