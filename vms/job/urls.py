from django.conf.urls import patterns, url
from job import views

urlpatterns = patterns('',
    url(r'^create/$', views.create, name='create'),
    url(r'^delete/(?P<job_id>\d+)$', views.delete, name='delete'),
    url(r'^details/(?P<job_id>\d+)$', views.details, name='details'),
    url(r'^edit/(?P<job_id>\d+)$', views.edit, name='edit'),
    url(r'^list/$', views.list, name='list'),
    url(r'^list_sign_up/(?P<event_id>\d+)/(?P<volunteer_id>\d+)$', views.list_sign_up, name='list_sign_up'),
)
