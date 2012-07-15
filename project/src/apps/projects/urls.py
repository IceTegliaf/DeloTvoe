from django.conf.urls import patterns, url

urlpatterns = patterns('apps.projects.views',
    url(r'^(?P<id>\d+)/$', 'project', name="project_card"),
    url(r'^list/$', 'projects', name="project_list"), 
)