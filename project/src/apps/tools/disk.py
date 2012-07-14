import subprocess
import re


class DiskInfo(object):
    
    class Info():
        def __init__(self, fs, total, usage, free, percent, mount):
            self.fs, self.total, self.usage, self.free, self.percent, self.mount = fs, long(total), long(usage), long(free), long(percent), mount
    
    def __init__(self):
        process = subprocess.Popen("df",
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        )
        data  = process.communicate()[0]
        self.data = re.findall("([\w\/]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\%\s+([\w\/]+)", data)
        
    def __iter__(self):
        for line in self.data:
            yield DiskInfo.Info(
                   line[0],
                   line[1],
                   line[2],
                   line[3],
                   line[4],
                   line[5],
                   )
            
            
    def for_file(self, filename):
        max_info = 0
        res_info = None
        for info in self:
            if filename.startswith(info.mount):
                if len(info.mount) > max_info:
                    max_info = len(info.mount)
                    res_info = info
                     
        return res_info
                     
        
        
        