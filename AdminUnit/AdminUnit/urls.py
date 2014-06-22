from django.conf.urls import patterns, url
from AdminUnit import views

urlpatterns = patterns('',
		url(r'^$', views.index),
		url(r'^register/$', views.register),
		url(r'^event/$', views.editEvent),
		url(r'^event/(?P<eventId>\d+)/$', views.editEvent),
		url(r'^deleteEvent/(?P<eventId>\d+)/$', views.deleteEvent),
		url(r'^allEvents/$', views.allEvents),
		url(r'^assignJob/$', views.assignJob),
		url(r'^assignJob/(?P<jobId>\d+)/$', views.assignJob),
		url(r'^allAssignedJobs/$', views.allAssignedJobs),
		url(r'^deleteJob/(?P<jobId>\d+)/$', views.deleteJob),
		url(r'^login/$', views.login_process),
		url(r'^logout/$', views.logout_process),
		)
