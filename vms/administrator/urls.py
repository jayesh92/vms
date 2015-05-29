from django.conf.urls import patterns, url
from administrator import views

urlpatterns = patterns('',
    url(r'^report/$', views.report, name='report'),
    url(r'^settings/$', views.settings, name='settings'),
)
