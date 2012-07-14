from apps.compressor.base import compressor
from apps.compressor.consts import COMPRESSOR_CACHE_ROOT, COMPRESSOR_MARKER
from django.conf import settings
import os
from django.views.static import serve



if not os.path.isdir(COMPRESSOR_CACHE_ROOT):
    raise Exception("No such file or directory: '%s'" % COMPRESSOR_CACHE_ROOT)


class CompressorMiddleware(object):
    
    def process_request(self, request):
        compressor.clean()
        
    def _apply(self, response, phase):
        if compressor.is_used():
            if settings.DEBUG:
                if response.content.find(COMPRESSOR_MARKER[phase])==-1:
                    raise Exception("Missing template tag 'compressed_%s' into template file." % phase)
                
            data = compressor.compress(phase)
        else:
            data = ""            
        try:
            response.content = response.content.replace(COMPRESSOR_MARKER[phase], data)
        except Exception, e:
            response.content = response.content.decode('utf8').replace(COMPRESSOR_MARKER[phase], data)

    def process_view(self, request, view_func, view_args, view_kwargs):
        request._apply_compresor = view_func != serve
        return None 
            
    def process_response(self, request, response):
        if response.status_code == 200 and (not hasattr(request,'_apply_compresor') or request._apply_compresor):
            self._apply(response, "js")
            self._apply(response, "css")
        return response 
