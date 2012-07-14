# coding=utf-8
from django import template
from django.utils.translation   import ugettext_lazy as _
from apps.staticpages.models import Page
from apps.tools.middleware import get_current_user
from django.template import TemplateSyntaxError, Node, Variable,\
    VariableDoesNotExist

register = template.Library()
  
@register.inclusion_tag('staticpages/included_page.html')
def staticpage(address):
    page, created = Page.objects.get_or_create(address = address, published = True,
                                               defaults={'title':address})
    return {
        'page': page,
        'user': get_current_user()
    }
    
    
    
class GetStaticPage(Node):

    def __init__(self, address, var_name):
        var = Variable(address)
        try:
            self.address =  var.resolve(var)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"get_static_page" tag got an unknown variable: %r' % var.var)
        
        self.var_name = var_name
        
        if not self.var_name:        
            raise TemplateSyntaxError('"get_static_page" tag got an empty result variable name')
        
    def render(self, context):
        page, created = Page.objects.get_or_create(address = self.address, published = True,
                                                   defaults={'title':self.address})
            
        context[self.var_name] = page
        return ""    


def get_static_page(parser, token):
    args = token.split_contents()
    if len(args)<4:
        raise TemplateSyntaxError('"get_static_page" got 3 arguments, get %s' % len(args))
        
    return GetStaticPage(args[1], args[3])
register.tag(get_static_page)