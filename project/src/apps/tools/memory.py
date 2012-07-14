import subprocess
import re

_scale = {'kB': 1, 'mB': 1024.0,
          'KB': 1, 'MB': 1024.0}



class UserMemoryMonitor(object):

    def __init__(self, username):
        """Create new MemoryMonitor instance."""
        self.username = username

    def usage(self):
        """Return int containing memory used by user's processes."""
        self.process = subprocess.Popen("ps -u %s -o rss | awk '{sum+=$1} END {print sum}'" % self.username,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        )
        self.stdout_list = self.process.communicate()[0].split('\n')
        return int(self.stdout_list[0])
    
    
class ProcMeminfo(object):
    
    def __init__(self):
        f=open("/proc/meminfo", "rt")
        res = re.findall("([\w\(\)]+):\s+(\d+)\s([k|K|B|M]*)", f.read())
        f.close()
        self.data={}
        for line in res:
            try:
                k = _scale[line[2]]
            except KeyError:
                k = 1
                
            self.data[line[0]]=int(line[1]) * k

    def __getitem__(self, name):
        return self.data[name] 
        
    def __iter__(self):
        for item in self.data.items():
            yield item
            
    
        