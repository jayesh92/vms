from django.conf.urls import patterns, url
from shift import views

urlpatterns = patterns('',
    url(r'^add_hours/(?P<shift_id>\d+)/(?P<volunteer_id>\d+)$', views.add_hours, name='add_hours'),
    url(r'^create/(?P<job_id>\d+)$', views.create, name='create'),
    url(r'^cancel/(?P<shift_id>\d+)/(?P<volunteer_id>\d+)$', views.cancel, name='cancel'),
    url(r'^delete/(?P<shift_id>\d+)$', views.delete, name='delete'),
    url(r'^clear_hours/(?P<shift_id>\d+)/(?P<volunteer_id>\d+)$', views.clear_hours, name='clear_hours'),
    url(r'^edit/(?P<shift_id>\d+)$', views.edit, name='edit'),
    url(r'^edit_hours/(?P<shift_id>\d+)/(?P<volunteer_id>\d+)$', views.edit_hours, name='edit_hours'),
    url(r'^list_jobs/$', views.list_jobs, name='list_jobs'),
    url(r'^list_shifts/(?P<job_id>\d+)$', views.list_shifts, name='list_shifts'),
    url(r'^list_shifts_sign_up/(?P<job_id>\d+)/(?P<volunteer_id>\d+)$', views.list_shifts_sign_up, name='list_shifts_sign_up'),
    url(r'^manage_volunteer_shifts/(?P<volunteer_id>\d+)$', views.manage_volunteer_shifts, name='manage_volunteer_shifts'),
    url(r'^sign_up/(?P<shift_id>\d+)/(?P<volunteer_id>\d+)$', views.sign_up, name='sign_up'),
    url(r'^view_hours/(?P<volunteer_id>\d+)$', views.view_hours, name='view_hours'),
    url(r'^view_volunteer_shifts/(?P<volunteer_id>\d+)$', views.view_volunteer_shifts, name='view_volunteer_shifts'),
    url(r'^volunteer_search/$', views.volunteer_search, name='volunteer_search'),
)
