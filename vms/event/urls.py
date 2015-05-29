from django.conf.urls import patterns, url
from event import views

urlpatterns = patterns('',
    url(r'^create/$', views.create, name='create'),
    url(r'^delete/(?P<event_id>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?P<event_id>\d+)$', views.edit, name='edit'),
    url(r'^list/$', views.list, name='list'),
    url(r'^list_sign_up/(?P<volunteer_id>\d+)$', views.list_sign_up, name='list_sign_up'),
)
