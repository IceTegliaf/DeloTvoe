import os
from apps.compressor.consts import COMPRESSOR_CACHE_ROOT
from apps.tools.check_settings import BaseCheck
from django.conf import settings


class Check(BaseCheck):
    
    path_exists =  [ settings.MEDIA_ROOT,
             COMPRESSOR_CACHE_ROOT ]
    
    file_creation = [ COMPRESSOR_CACHE_ROOT ]
    
    middlewares = ["apps.compressor.middleware.CompressorMiddleware"]
    
    #TODO: add check 'coffee' installed if CoffeeScript used
