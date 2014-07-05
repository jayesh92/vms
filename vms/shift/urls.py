from django.conf.urls import patterns, url
from shift import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add_hours/(?P<shift_id>\d+)/(?P<volunteer_id>\d+)/$', views.add_hours, name='add_hours'),
    url(r'^authorization_error/$', views.authorization_error, name='authorization_error'),
    url(r'^cancel_shift/(?P<shift_id>\d+)/(?P<volunteer_id>\d+)/$', views.cancel_shift, name='cancel_shift'),
    url(r'^create_shift/(?P<job_id>\d+)/$', views.create_shift, name='create_shift'),
    url(r'^error/$', views.error, name='error'),
    url(r'^shift_sign_up/(?P<shift_id>\d+)/$', views.shift_sign_up, name='shift_sign_up'),
    url(r'^view_volunteer_shifts/(?P<volunteer_id>\d+)/$', views.view_volunteer_shifts, name='view_volunteer_shifts'),
    url(r'^view_hours/(?P<shift_id>\d+)/(?P<volunteer_id>\d+)/$', views.view_hours, name='view_hours'),
)
