"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from JiaBlog import views
from channels.routing import ProtocolTypeRouter
import debug_toolbar

# from django.views import static

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})

urlpatterns = [
    url(r'^$', views.blog_index),
    url(r'^baidu_verify_iYpMqoGJf4.html/$', views.baiduyz),
    path('admin/', admin.site.urls),
    path('JiaBlog/', include('JiaBlog.urls', namespace="JiaBlog")),
    path('activemq/', include('activemq.urls', namespace="activemq")),
    path('online-intepreter/', include('online_intepreter.urls', namespace="online_intepreter")),
    path('mdeditor/', include('mdeditor.urls')),
    path('china-wuhan/', views.china_wuhan),
    path('china-wuhan/virusdata', views.china_wuhan_virus),
    url(r'', include('social_django.urls', namespace='social')),
    # url(r'^oauth/', include('social_django.urls', namespace='social')),
    # url(r'^search/', include('haystack.urls')),                   # old way
    url(r'^search/', views.MySeachView(), name='haystack_search'),  # new way
    path(r"__debug__/", include(debug_toolbar.urls)),
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}, name='static'),
    # url(r'^media/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
