from django.conf.urls import url, re_path
from oblog import views
from werobot.contrib.django import make_view
from oblog import newrobot
from oblog import robot
from django.conf import settings

app_name = 'oblog'
urlpatterns = [
    url(r'^search/$', views.search),
    url('^$', views.blog_index, name='index'),
    url(r'^index/$', views.blog_index),
    url(r'^about/$', views.aboutme),
    url(r'^article/(?P<article_id>[0-9]+)/$', views.blog_info),
    # url(r'^weather/$',views.getlocalweather),
    # url(r'love/',views.getlove),
    # url(r'lovepic/',views.getlovepic),
    url(r'^document/', views.getdocument),
    url(r'^robot/', views.weixin),
    url(r'^mymenu/', views.mymenu),
    url(r'^download/$', views.file_down, name='download'),
    url(r'^email/', views.sendemail),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^new/', views.newindex),
    url(r'^monitor/', views.monitor),
    url(r'^savemessage/', views.savemessage),
    url(r'^inputtranslate/', views.inputtranslate),
    url(r'^translate/', views.translate),
    url(r'^videotest/', views.videotest),
    url(r'^film/', views.movie_list, name="movie"),
    url(r'^videoplayer/(?P<film_name>.+)/$', views.videoplayer),
    url(r'^article/(?P<article_id>[0-9]+)/comment', views.comment_view, name='comment'),
    url(r'^time/', views.timeline),
    url(r'^greats/(?P<article_id>[0-9]+)', views.greats),
    url(r'^list/', views.blog_list),
    url(r'^articles/(.+)/$', views.blog_category),

]
