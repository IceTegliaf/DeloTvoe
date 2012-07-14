from django.conf import settings
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
    
    
if 'apps.tools.middleware.GlobalRequest' not in settings.MIDDLEWARE_CLASSES:
    raise Exception("Put 'apps.tools.middleware.GlobalRequest' into your settings.MIDDLEWARE_CLASSES")

_thread_locals = local()
def get_current_user():
    return getattr(_thread_locals, 'user', None)

def get_request():
    return getattr(_thread_locals, 'request', None)

class GlobalRequest(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        _thread_locals.request = request

