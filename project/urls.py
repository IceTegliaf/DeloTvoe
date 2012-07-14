# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', "apps.projects.views.index", name="projects_index"),
        
    url(r'^feedback', include('apps.simple_feedback.urls')),
    url(r'^project', include('apps.projects.urls')),                       
#    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^tinymce/', include('tinymce.urls')),


    url(r'^', include('apps.staticpages.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes = True)
    urlpatterns += staticfiles_urlpatterns()

    
