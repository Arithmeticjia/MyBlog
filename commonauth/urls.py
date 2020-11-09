from django.conf.urls import url, include
from django.urls import path
from commonauth import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

app_name = 'commonauth'


urlpatterns = [
    url(r'^login/$', views.do_login, name='login'),
]
