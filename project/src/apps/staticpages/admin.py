# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.staticpages.models import *
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.template.loader import render_to_string

class PageAdmin(admin.ModelAdmin):
    model = Page
    list_display = ('title', 'address', 'published', 'address_link', 'show_title' )
    list_filter  = ('published', )
    list_editable = ('published', 'show_title')
    prepopulated_fields = {'address': ('title',)}
    fieldsets = [
        (None, {
            'fields': ['title','show_title', 'address', 'content', 'published',]
        }),
        (_('SEO options'), {
            'classes': ['collapse'],
            'fields': ['seo_title', 'seo_keywords', 'seo_description']
        }),
    ]
    
    class Media:
        js = (
              '/static/fckeditor/fckeditor.js',
              '/static/fckeditor/_media/textarea_all.js',
              )
              
#    def changelist_view(self, request, extra_context=None):
#        
#        if request.POST and 'action' in request.POST:
#            if request.POST['action']=='checkbox_invert':
#                model = self.model
#                obj = model.objects.get(pk=request.POST['id'])
#                value = getattr(obj, request.POST['field'])
#                newValue = not value
#                setattr(obj, request.POST['field'], newValue)
#                obj.save()
#                return HttpResponse(u'%d' % newValue)
#
#        
#        if not extra_context: extra_context={}
#        extra_context.update({
#                              'media':mark_safe(self.media),
#                              })
#        
#        return super(PageAdmin, self).changelist_view(request, extra_context)
    
    
    def address_link(self, obj):
        return obj.get_absolute_url()
            
    address_link.allow_tags = True
    address_link.short_description = _('link')
    
#    # PUBLISHED custom admin column
#    def my_tag_published(self, obj):
#        out = {}
#        out['name'] = 'published'
#        out['self'] = obj
#        out['parameter'] = obj.published
#        return render_to_string('admin/interfaces/checkbox.html', out)
#                
#    my_tag_published.allow_tags = True
#    my_tag_published.short_description = _('published')
#    
#    # DELETE TAG
#    def my_tag_delete(self, obj):
#        out={}
#        out['id'] = obj.id
#        return render_to_string('admin/interfaces/button_delete.html', out)
#                
#    my_tag_delete.allow_tags = True
#    my_tag_delete.short_description = _('Delete?')    
    
admin.site.register(Page, PageAdmin)