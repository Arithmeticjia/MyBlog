from django.conf.urls import url,include
from cloudserver import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^chart/$', views.chart, name='chart'),
    url(r'^chart_pred/$', views.chart_pred, name='chart'),
    url(r'^chart_json/$', views.chart_json, name='chart_json'),
    url(r'^server_cpu_json/$', views.server_cpu_json, name='server_json'),
    url(r'^server_cpu_pred_json/$', views.server_cpu_pred_json, name='server_json'),
    url(r'^server_mem_json/$', views.server_mem_json, name='server_json'),
]
