from django.conf.urls import patterns, url
from job import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^authorization_error/$', views.authorization_error, name='authorization_error'),
    url(r'^create_job/$', views.create_job, name='create_job'),
    url(r'^create_shift/(?P<job_id>\d+)/$', views.create_shift, name='create_shift'),
    url(r'^details/(?P<job_id>\d+)/$', views.details, name='details'),
    url(r'^error/$', views.error, name='error'),
    url(r'^list_jobs/$', views.list_jobs, name='list_jobs'),
    url(r'^manage_jobs/$', views.manage_jobs, name='manage_jobs'),
    url(r'^shift_sign_up/(?P<shift_id>\d+)/$', views.shift_sign_up, name='shift_sign_up'),
    url(r'^view_volunteer_shifts/(?P<volunteer_id>\d+)/$', views.view_volunteer_shifts, name='view_volunteer_shifts'),
)
