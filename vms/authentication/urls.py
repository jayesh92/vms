from django.conf.urls import patterns, url
from authentication import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_process, name='login_process'),
    url(r'^logout/$', views.logout_process, name='logout_process'),
)
