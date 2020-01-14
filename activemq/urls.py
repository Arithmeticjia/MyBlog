from django.conf.urls import url, include
from activemq import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'activemq'


urlpatterns = [
    url(r'^send/task/(?P<task_id>[0-9]+)/$', views.send_to_queue),
    url(r'^listen/(?P<queue_id>[0-9]+)/$', views.listen_from_queue),
    url(r'^test/(?P<task_id>[0-9]+)/$/$', views.testactivemq),
]




