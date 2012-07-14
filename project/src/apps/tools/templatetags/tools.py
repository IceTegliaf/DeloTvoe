# coding: utf-8
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.utils.dateformat import format
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _, ugettext
from pytils import numeral
import datetime
import string
import sys
from apps.tools import human_dt

register = template.Library()



@register.filter_function
def human_date(var):
    return human_dt.human_date(var)


@register.filter_function
def human_datetime(var):
    return human_dt.human_datetime(var)


@register.simple_tag
def trans_class_vn_plural(cls):
    parts = string.split(force_unicode(cls._meta.verbose_name_plural))
    parts[0] = string.capitalize(parts[0])
    return ' '.join(parts)

    
@register.simple_tag
def trans_class_vn(cls):
    parts = string.split(force_unicode(cls._meta.verbose_name))
    parts[0] = string.capitalize(parts[0])
    return ' '.join(parts)

    
@register.simple_tag
def class_raw_vn_name(cls):
    return cls._meta.verbose_name_raw


@register.filter
@stringfilter
def strip(value):
    return value.strip()
    

@register.simple_tag
def trans_app_name(app_name):
    app_name = app_name.lower()
    if app_name == 'auth':
        return ugettext(u'users')
    elif app_name == 'comments':
        return ugettext(u'comments')
    else:
        try:
            app = sys.modules[app_name]
            return app.app_label.capitalize()
        except:
            try:
                app = sys.modules["apps.%s" % app_name]
                return app.app_label.capitalize()
            except:
                return app_name.capitalize()
                
  
@register.inclusion_tag('utils/admin_btn.html', takes_context=True)
def admin_btn(context, app, model, id):
    try:
        from apps.langs.models import get_cur_lang
    except:
        get_cur_lang = None
        
        
    try:
        admin_url = reverse("admin:%s_%s_change" % (app, model), args=[id])
    except:
        admin_url = "/admin/%s/%s/%s/" % (app, model, id)
        
    return {
        'app': app,
        'model':model,
        'id':id,
        'admin_url':admin_url,
        'user': context['user'],
        'cur_lang': get_cur_lang() if get_cur_lang else None
    }
    
def number_format(number, decimals=0, dec_point='.', thousands_sep=' '):
    try:
        number = round(float(number), int(decimals))
    except ValueError:
        return number
    neg = number < 0
    integer, fractional = str(abs(number)).split('.')
    m = len(integer) % 3
    if m:
        parts = [integer[:m]]
    else:
        parts = []
    
    parts.extend([integer[m+t:m+t+3] for t in xrange(0, len(integer[m:]), 3)])
    
    if decimals:
        return '%s%s%s%s' % (
            neg and '-' or '', 
            thousands_sep.join(parts), 
            dec_point, 
            fractional.ljust(decimals, '0')[:decimals]
        )
    else:
        return '%s%s' % (neg and '-' or '', thousands_sep.join(parts))

register.filter(number_format)


@register.simple_tag
def progress(value, all):
    if all:
        return int(float(value) / all * 100)
    return 0


class VerbatimNode(template.Node):
    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


@register.tag
def verbatim(parser, token):
    text = []
    while True:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        elif token.contents.find('trans') == 0:
            text.append(ugettext(token.contents[7:-1]))
        elif token.contents.find('trans') != 0:
            if token.token_type == template.TOKEN_VAR:
                text.append('{{')
            elif token.token_type == template.TOKEN_BLOCK:
                text.append('{%')
            text.append(token.contents)
            if token.token_type == template.TOKEN_VAR:
                text.append('}}')
            elif token.token_type == template.TOKEN_BLOCK:
                text.append('%}')
    return VerbatimNode(''.join(text))
