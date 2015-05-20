from django.conf.urls import patterns, url
from organization import views

urlpatterns = patterns('',
    url(r'^create/$', views.create, name='create'),
    url(r'^delete/(?P<organization_id>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?P<organization_id>\d+)$', views.edit, name='edit'),
    url(r'^list/$', views.list, name='list'),
)
