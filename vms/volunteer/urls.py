from django.conf.urls import patterns, url
from volunteer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),    
    url(r'^create/$', views.create, name='create'),
    url(r'^delete/(?P<volunteer_id>\d+)/$', views.delete, name='delete'),
    url(r'^delete_resume/(?P<volunteer_id>\d+)/$', views.delete_resume, name='delete_resume'),
    url(r'^download_resume/(?P<volunteer_id>\d+)/$', views.download_resume, name='download_resume'),
    url(r'^edit/(?P<volunteer_id>\d+)/$', views.edit, name='edit'),
    url(r'^error/$', views.error, name='error'),
    url(r'^list/$', views.list, name='list'),
    url(r'^options/$', views.options, name='options'),
    url(r'^profile/(?P<volunteer_id>\d+)/$', views.profile , name='profile'),
    url(r'^search/$', views.search, name='search'),
)
