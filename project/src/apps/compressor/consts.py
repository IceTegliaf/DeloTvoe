from apps.tools.shortcuts import get_settings
from django.conf import settings
import os


PROCESSOR_LIST = get_settings("COMPRESSOR_PROCESSORS", [
    "apps.compressor.coffee_script.CoffeeCompiler",
    "apps.compressor.processors.OneFile",
    "apps.compressor.processors.Inline",
    "apps.compressor.processors.Links",    
])





COMPRESSOR_MODE_ONE_FILE = 1
COMPRESSOR_MODE_LINKS = 2 
COMPRESSOR_MODE_INLINE =3 


COMPRESSOR_MARKER = {
                     "css": "<!--[*CSS*]-->",
                     "js":  "<!--[*JS*]-->"
                     }


COMPRESSOR_CACHE_PREFIX = "cache"

COMPRESSOR_CACHE_ROOT = get_settings('COMPRESSOR_CACHE_ROOT', os.path.join(settings.MEDIA_ROOT, COMPRESSOR_CACHE_PREFIX))
COMPRESSOR_CACHE_URL  = get_settings('COMPRESSOR_CACHE_URL', settings.MEDIA_URL + COMPRESSOR_CACHE_PREFIX + '/')
COMPRESSOR_ONE_FILE_IGNORE = get_settings("COMPRESSOR_ONE_FILE_IGNORE", [])

FILE_MARKER = "//__file__="