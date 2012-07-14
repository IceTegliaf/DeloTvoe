# coding: utf-8
from apps.projects.models import Project
__author__ = "Kovalenko Pavel <pavel@bitrain.ru>"
__date__ = "$Date: 2011-09-15 13:00:23 +0400 (Чт, 15 сен 2011) $"
__version__ = "$Rev: 7036 $"

from django.contrib import admin


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','importance','is_enable')
    list_filter = ('is_enable',)
    search_fields = ("name", 'description')
    list_editable = ('is_enable', 'importance')
    
    class Media:
        js = (
              '/static/fckeditor/fckeditor.js',
              '/static/fckeditor/_media/textarea_all.js',
              )    
    
admin.site.register(Project, ProjectAdmin)