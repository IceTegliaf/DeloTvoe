from django.core.management.color import color_style
from django.utils.encoding import force_unicode
import sys
import time


def print_sql_queries():
    style = color_style()
    from django.db import connection
    i=1
    for query in connection.queries:
        sql = force_unicode(query['sql'])
        sys.stdout.write(style.NOTICE(force_unicode(u'%03d:    %s: %s\n\n' % (i, force_unicode(query['time']), sql))))
        i=i+1


class Timer():
    def __init__(self, name=""):
        self.begin = time.time()
        self.name = name
        
    def finish(self):
        return (time.time() - self.begin)*1000
    
    def log(self):
        str = "%s Finish: %s ms" % (self.name, self.finish())
        print str
        return str