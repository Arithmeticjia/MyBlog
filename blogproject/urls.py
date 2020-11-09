from django.conf.urls import url, include
from django.urls import path
from blogproject import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

app_name = 'blogproject'


urlpatterns = [
    url(r'^post/(?P<article_id>[0-9]+)/(?P<url_slug>[-\w]+)/$', views.post_detail, name='post'),
    url(r'^auth/$', views.check_auth, name='auth'),
]
