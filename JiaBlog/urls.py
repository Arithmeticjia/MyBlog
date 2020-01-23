from django.conf.urls import url,include
from JiaBlog import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

app_name = 'JiaBlog'

# 定义restfulapi的路由地址
route = routers.DefaultRouter()

# 注册restfulapi的路由地址
route.register(r'getarticleinfo', views.GetArticleInfo)
# route.register(r'getweatherinfo', views.GetWeatherInfo)

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^search/', views.MySeachView(), name='haystack_search'),
    url(r'^index/$', views.blog_index),
    url(r'^article/(?P<article_id>[0-9]+)/(?P<slug>[-\w]+)/$', views.blog_info),
    url(r'^list/$',views.blog_list),
    url(r'^article/(?P<article_id>[0-9]+)/comment/(?P<cid>.+)',views.comment_view,name='comment'),
    url(r'^contact-us/$',views.contact),
    url(r'^savemessage/$',views.savemessage),
    url(r'^articles/(.+)/$', views.blog_category),
    url(r'^greats/$',views.greats),
    url(r'^admin/$', views.admininndex),
    url(r'^admincharts/$', views.admincharts),
    url(r'^login/$', views.login_view,name='login'),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^register/$', views.register_view),
    url(r'^search/$', views.search),
    url(r'^upload_file/$', views.upload_file),
    url(r'^JiaFile/$', views.Jiafile),
    url(r'^article/(?P<article_id>[0-9]+)/(?P<slug>[-\w]+)/editor/$', views.usereditor),
    url(r'^article/(?P<article_id>[0-9]+)/(?P<slug>[-\w]+)/editor/save/$', views.article_save),
    url(r'^mylist/$', views.mylist),
    url(r'^mylist/(?P<article_status>.+)/$', views.mylist_para),
    url(r'^article/editor/create/$', views.article_create),
    url(r'^article/editor/create/save/$', views.article_create_save),
    url(r'^article/(?P<article_id>[0-9]+)/(?P<slug>[-\w]+)/editor/delete/', views.article_delete),
    url(r'^article/(?P<article_id>[0-9]+)/(?P<slug>[-\w]+)/cancelcollect/', views.cancelcollect),
    url(r'^editor/userbrief/$', views.editor_userbrief),
    url(r'^editor/addcategory/$', views.editor_addcategory),
    url(r'^myadmin/$', views.my_admin),
    url(r'^cal/$', views.calculate),
    url(r'^onlineeditor/$', views.pyeditor),
    url(r'^api/$',views.api),
    url(r'^upload_images/(?P<article_id>[0-9]+)/$', views.upload_images),
    url(r'^recruitment/$',views.recruitment),
    url(r'^recruitment/info/$',views.recruitmentinfo),
    url(r'^recruitment/findme/$',views.findme),
    url(r'^film/', views.movie_list, name="movie"),
    url(r'^deletefile/$', views.deletefile),
    url(r'^ajfileupload/$', views.ajupload_file),
    url(r'^filecheck/$', views.filecheck),
    url(r'^list/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.blog_time),
    url(r'^weather/', views.getlocalweather),
    url(r'^jiadmin/', views.JiaAdmin.as_view()),
    url(r'^post/(?P<article_id>[0-9]+)/$', views.JiaPost.as_view()),
    url(r'^test/', views.JiaIndex.as_view()),
    url(r'^resume/', views.Resume.as_view()),
    # url(r'^getweatherinfo/', views.GetWeatherInfo.as_view()),
    url(r'^getweatherinfo/', csrf_exempt(views.GetWeatherInfo.as_view()),name='getweatherinfo'),
    url('api/', include(route.urls)),
    url(r'^collect/$', views.collect),
    url(r'^comments/(?P<article_id>[0-9]+)$',views.comments),

]




