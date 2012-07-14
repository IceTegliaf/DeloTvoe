from apps.projects.models import Project
from apps.tools.decorators import render_to
from django.shortcuts import get_object_or_404

@render_to
def index(request):
    return {}


@render_to
def projects(request):
    return {'projects': Project.objects.filter(is_enable = True).order_by('importance')}

@render_to
def project(request, id):
    return {'project': get_object_or_404(Project, pk = id) }
    