from django.conf.urls import url, include
from itube import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt


app_name = 'itube'

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^video/(?P<video_id>[0-9]+)/$', views.single_video),
    url(r'^video/single/(?P<video_id>[0-9]+)/$', views.single_video_new),
]




