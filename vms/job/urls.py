from django.conf.urls import patterns, url
from job import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^authorization_error/$', views.authorization_error, name='authorization_error'),
    url(r'^confirmation/$', views.confirmation, name='confirmation'),
    url(r'^create/$', views.create, name='create'),
    url(r'^details/$', views.details, name='details'),
    url(r'^error/$', views.error, name='error'),
    url(r'^list/$', views.list, name='list'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
)
