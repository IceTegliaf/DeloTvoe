import hashlib
import types
from django.core.files.uploadedfile import UploadedFile

BUFFER_SIZE = 2048

def get_file_md5(file):
    filehash = hashlib.md5()
    if isinstance(file, types.StringTypes):
        f = open(file,'rb')
    elif isinstance(file, UploadedFile):
        f = file

    while True:
        data = f.read(BUFFER_SIZE)
        if len(data) == 0:
            break
        filehash.update(data)
        
    if isinstance(file, types.StringTypes):
        f.close()
    return filehash.hexdigest()