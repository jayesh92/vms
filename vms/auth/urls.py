from django.conf.urls import url
from auth import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_volunteer/$', views.register_volunteer, name='register_volunteer'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
]
