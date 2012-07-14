from apps.tools.class_loader import get_class_by_string
from django.conf import settings
import os
import sys
from django.core.management.color import color_style
import pwd
from django.utils.encoding import force_unicode
import stat

class CheckSettingsException(Exception):
    pass

class PathNotExists(CheckSettingsException):
    
    def __init__(self, path):
        self.path = path        
    __unicode__ = lambda self: "No such file or directory '%s'" % self.path
    

class PutInMiddleware(CheckSettingsException):
    
    def __init__(self, name):
        self.name = name
    __unicode__ = lambda self:  "Put '%s' in your settings.MIDDLEWARE_CLASSES" % self.name

class WrongDirGroup(CheckSettingsException):
    
    def __init__(self, gid, dir):
        self.gid = gid
        self.dir = dir
        
    def __unicode__(self):
        user = pwd.getpwuid(self.gid)
        return "Set group '%s' (gid:%s) to directory '%s'" % (user.pw_name, self.gid, self.dir)
        
class FileCreationError(CheckSettingsException):
    def __init__(self, dir):
        self.dir = dir
        
    def __unicode__(self):
        user = pwd.getpwuid(os.getuid())
        return "Can't create file in '%s'. current uid:%s, user:%s" % (self.dir, os.getuid(), user.pw_name)
        
class DuplicateProcess(CheckSettingsException):
    
    def __init__(self, pidfile, process_name):
        self.pidfile = pidfile
        self.process_name = process_name
        
    def __unicode__(self):
        return "Process '%s' already running. For check using '%s'" % (self.process_name, self.pidfile) 
    
class DefineSettings(CheckSettingsException):
    
    def __init__(self, name):
        self.name = name
        
    def __unicode__(self):
        return "Define settings.%s" % self.name
    
class InstallPythonModule(CheckSettingsException):
    
    def __init__(self, name):
        self.name = name
        
    def __unicode__(self):
        return "Install python module '%s'" % self.name    
    
class InstallApp(CheckSettingsException):
    
    def __init__(self, name):
        self.name = name
        
    def __unicode__(self):
        return "Put '%s' in your settings.INSTALLED_APPS" % self.name
    
               
class BaseCheck(object):
    path_exists = []
    middlewares = []
    file_creation = []
    define_settings = []
    python_module = []
    installed_apps = []
    group_execute = []

    def check_group_execute_permission(self, path):
        path_stat = os.stat(path)
        if (path_stat.st_mode & stat.S_IXGRP) != stat.S_IXGRP:
            raise Exception("Set 'g+x' mode for group to directory '%s'" % (path))
        
    def check_path_exists(self, path):
        if not os.path.exists(path):
            raise PathNotExists(path)
        
    def check_middleware(self, name):
        if name not in settings.MIDDLEWARE_CLASSES:
            raise PutInMiddleware(name)
        
    # def check_middleware(self, name):
    #     if name not in settings.TEMPLATE_CONTEXT_PROCESSORS:
    #         raise PutInMiddleware(name)
                
    def check_dir_group(self, path, gid):
        sites_dir = os.stat(path)
        if sites_dir.st_gid!=gid:
            raise WrongDirGroup(gid, path)
        
    def chkec_file_creation(self, path):
        test_filename = os.path.join(path, "test.file")
        try:
            f = open(test_filename, "wt")
            f.close()
            os.unlink(test_filename)
        except IOError, e:            
            raise FileCreationError(path)
        
    def check_duplicate_process(self, pid_file, process_name):
        try:
            f=open(pid_file, "rt")
            mypid = int(f.read())
            f.close()        
        except IOError:
            mypid = None
            
        if os.path.exists("/proc/%s" % mypid):
            raise DuplicateProcess(pid_file, process_name)
        
    def check_settings(self, name):
        if not hasattr(settings, name):
            raise DefineSettings(name)
   
    def check_python_module(self, name):
        if name in sys.modules:
            return     
        try:
            __import__(name)
        except ImportError:
            raise InstallPythonModule(name)
    
    def check_installed_app(self, name):
        if name not in settings.INSTALLED_APPS:
            raise InstallApp(name)
                    
    
    def run(self):
        for value in self.path_exists:
            self.check_path_exists(value)
            
        for value in self.middlewares:
            self.check_middleware(value)
            
        for valie in self.file_creation:
            self.chkec_file_creation(valie)
            
        for value in self.define_settings:
            self.check_settings(value)

        for value in self.python_module:
            self.check_python_module(value)
        
        for value in self.installed_apps:
            self.check_installed_app(value)
            
        for value in self.group_execute:
            self.check_group_execute_permission(value)
            
        self.custom()
        
    def custom(self):
        pass
             

     
def run_chekers():
    is_ok = True
    style = color_style()
    for app in settings.INSTALLED_APPS:
        if app=='apps.tools':
            continue;
        
        try:
            klass = get_class_by_string("%s.check_settings.Check" % app)
        except ImportError:
            continue
        except Exception, e:
            sys.stderr.write(style.ERROR("%s\n" % unicode(e)))
            from apps.ice_logger.global_log import log
            log.exception(e)
            continue

            
        if klass:            
            try:
                obj = klass()
                obj.run()
            except Exception, e:
                is_ok = False
                
                try:
                    sys.stderr.write(style.ERROR("%s\n" % force_unicode(e)))
                    
                    from apps.ice_logger.global_log import log
                    log.exception(e)
                    
                except Exception, ee:
                    sys.stderr.write(style.ERROR("Exception in show excaption '%s'\n" % type(e)))
                    sys.stderr.write(style.ERROR("%s" % ee))
                
                
    return is_ok
    
            
            
    