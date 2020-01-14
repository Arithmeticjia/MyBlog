from django.conf.urls import url, include
from activemq import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'activemq'


urlpatterns = [
    url(r'^send/$', views.send_to_queue),
    url(r'^listen/$', views.listen_from_queue),
]




