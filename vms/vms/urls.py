from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^job/', include('job.urls', namespace="job")),
    url(r'^organization/', include('organization.urls', namespace="organization")),
    url(r'^shift/', include('shift.urls', namespace="shift")),
    url(r'^volunteer/', include('volunteer.urls', namespace="volunteer")),
    url(r'^auth/', include('auth.urls', namespace="auth")),
)
