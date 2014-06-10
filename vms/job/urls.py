from django.conf.urls import patterns, url
from job import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^list/$', views.list_jobs, name='list_jobs'),
)
