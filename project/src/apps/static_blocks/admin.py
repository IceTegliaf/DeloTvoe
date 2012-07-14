# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from apps.static_blocks.models import Block


class BlockAdmin(admin.ModelAdmin):
    list_display = ('title','site', 'address', 'use_title')
    list_filter = ('site',)
#    prepopulated_fields = {'address': ('title',)}
    fieldsets = [
        (None, {
            'fields': ['title','use_title', 'content', ]
        }),
    ]
    class Media:
        js = (
              '/media/fckeditor/fckeditor.js',
              '/media/fckeditor/_media/textarea_all.js',
              )
#        js = (
#              '/media/ckeditor/fckeditor.js',
#              '/media/js/textarea_all.js',
#              '/media/js/jquerymin.js',
#              '/media/js/java.js',
#              '/media/js/admin/change_list_controls.js',
#              )
              
admin.site.register(Block, BlockAdmin)