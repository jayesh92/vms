from django.conf.urls import patterns, url
from volunteer import views

urlpatterns = patterns('',
    url(r'^delete_resume/(?P<volunteer_id>\d+)$', views.delete_resume, name='delete_resume'),
    url(r'^download_resume/(?P<volunteer_id>\d+)$', views.download_resume, name='download_resume'),
    url(r'^edit/(?P<volunteer_id>\d+)$', views.edit, name='edit'),
    url(r'^profile/(?P<volunteer_id>\d+)$', views.profile , name='profile'),
    url(r'^report/(?P<volunteer_id>\d+)$', views.report, name='report'),
    url(r'^search/$', views.search, name='search'),
)
