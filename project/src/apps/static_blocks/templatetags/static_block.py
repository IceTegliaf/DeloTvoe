# coding=utf-8
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.template import Node, TemplateSyntaxError, Variable, \
    VariableDoesNotExist
from django.template.loader import render_to_string, get_template_from_string
from django.utils.translation import ugettext_lazy as _
from apps.static_blocks.models import Block, STATIC_BLOCKS_USE_CACHE, \
    STATIC_BLOCKS_CACHE_KEY, STATIC_BLOCKS_CACHE_TIMEOUT
from apps.tools.middleware import get_current_user
from apps.tools.shortcuts import get_settings




#REQUIRED = 'django.core.context_processors.auth'
#if REQUIRED not in settings.TEMPLATE_CONTEXT_PROCESSORS:
#    raise Exception('You must add %s to settings.TEMPLATE_CONTEXT_PROCESSORS if you want use threadlocals' % REQUIRED)



register = template.Library()

def get_or_create_block(address):    
    site = Site.objects.get_current()
    if STATIC_BLOCKS_USE_CACHE:  
        cache_key = STATIC_BLOCKS_CACHE_KEY % (address, site.id)       
        data = cache.get(cache_key)
        if data:
            block = Block()
            block.load_from_cache(data)
            return block            
        
    block, created = Block.objects.get_or_create(address = address, site = site)
    if created:
        block.title = address
        block.save()
        
    if STATIC_BLOCKS_USE_CACHE:
        cache.set(cache_key, block.save_to_cache(), STATIC_BLOCKS_CACHE_TIMEOUT)        
        
    return block
  
@register.inclusion_tag('static_blocks/block.html', takes_context = True)
def static_block(context, address):
    block = get_or_create_block(address)
    return {
        'block': block,
        'user': context['user'] if 'user' in context else (context['request'].user if 'request' in context and hasattr(context['request'], "user") else None) 
    }
    
    
    
@register.simple_tag
def get_static_block_title(address):
    return get_or_create_block(address).title


@register.simple_tag
def get_static_block_text(address):
    return get_or_create_block(address).content


class GetStaticBlock(Node):

    def __init__(self, address, var_name):
        var = Variable(address)
        try:
            self.address =  var.resolve(var)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"get_static_block" tag got an unknown variable: %r' % var.var)
        
        self.var_name = var_name
        
        if not self.var_name:        
            raise TemplateSyntaxError('"get_static_block" tag got an empty result variable name')
        
    def render(self, context):
        context[self.var_name] = get_or_create_block(self.address)
        return ""    

    


def get_static_block(parser, token):
    args = token.split_contents()
    if len(args)<4:
        raise TemplateSyntaxError('"get_static_block" got 3 arguments, get %s' % len(args))
        
    return GetStaticBlock(args[1], args[3])
register.tag(get_static_block)

class GetTplStaticBlock(Node):
    """Template instance for static_block with templates"""
    def __init__(self, address, var_name):
        var = Variable(address)
        try:
            self.address =  var.resolve(var)
        except VariableDoesNotExist:
            raise TemplateSyntaxError('"get_static_block" tag got an unknown variable: %r' % var.var)

        self.var_name = var_name

        if not self.var_name:
            raise TemplateSyntaxError('"get_static_block" tag got an empty result variable name')

    def render(self, context):
        block = get_or_create_block(self.address)
        context[self.var_name] = {
            'title': get_template_from_string(block.title).render(context),
            'content': get_template_from_string(block.content).render(context),
        }
        return ""

@register.tag()
def get_tpl_static_block(parser, token):
    args = token.split_contents()
    if len(args)<4:
        raise TemplateSyntaxError('"get_static_block" got 3 arguments, get %s' % len(args))

    return GetTplStaticBlock(args[1], args[3])