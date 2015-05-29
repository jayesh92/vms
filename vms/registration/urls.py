from django.conf.urls import patterns, url
from registration import views

urlpatterns = patterns('',
    url(r'^signup_administrator/$', views.signup_administrator, name='signup_administrator'),
    url(r'^signup_volunteer/$', views.signup_volunteer, name='signup_volunteer'),
)
