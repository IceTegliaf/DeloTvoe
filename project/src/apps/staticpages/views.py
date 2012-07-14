from apps.staticpages.models import Page
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from apps.tools.decorators import render_to



@render_to
def page(req, address, path_address=''):
    out={}
#    out['my_extends']='base.html'
    if settings.DEBUG and req.user.is_authenticated() and req.user.is_superuser:
        page, created = Page.objects.get_or_create(address = address, published = True)
        if created:
            page.title = address
            page.save()
    else:
        page = get_object_or_404(Page, address=address, published=True)

#    if page.extends:
#        out['my_extends']=page.extends
        
        
    out['page'] = page 
    return out
