from apps.projects.models import Project

class ProjectProcessor(object):
    
    def __init__(self, request):
        self.request = request
        
    def actual(self):
        return Project.objects.filter(is_enable = True)[:16]

def cp_projects(request):
    return {"cp_projects": ProjectProcessor(request)}