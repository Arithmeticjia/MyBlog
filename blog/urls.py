from django.conf.urls import url, include
from django.urls import path
from blog import views
from rest_framework import routers

app_name = 'blog'

# 定义restful的路由地址
router = routers.DefaultRouter()

# 注册restful的路由地址
router.register(r'getarticleinfo', views.GetArticleInfo)
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r"search", views.PostSearchView, basename="search")

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^api/', include(router.urls)),
    path('api/index/', views.IndexPostListAPIView.as_view()),
    # path('api/single/', views.PostViewSet.as_view({'get': 'retrieve'})),
    path('api/auth/', include("rest_framework.urls", namespace="rest_framework")),
    url(r'^search/', views.MySearchView(), name='haystack_search'),
    url(r'^index/$', views.blog_index),
    url(r'^article/(?P<article_id>[0-9]+)/(?P<slug>[-\w]+)/$', views.blog_info, name='article'),
    url(r'^list/$', views.blog_list),
    url(r'^article/(?P<article_id>[0-9]+)/comment/(?P<cid>.+)', views.comment_view, name='comment'),
    url(r'^contact-us/$', views.contact),
    url(r'^savemessage/$', views.savemessage),
    url(r'^articles/(.+)/$', views.blog_category),
    url(r'^greats/$', views.greats),
    url(r'^admin/$', views.admininndex),
    url(r'^admincharts/$', views.admincharts),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^register/$', views.register_view),
    url(r'^upload_file/$', views.upload_file),
    url(r'^file/$', views.Jiafile),
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
    url(r'^onlineeditor/$', views.pyeditor),
    url(r'^api/$', views.api),
    url(r'^upload_images/(?P<article_id>[0-9]+)/$', views.upload_images),
    url(r'^recruitment/$', views.recruitment),
    url(r'^recruitment/info/$', views.recruitment_info),
    url(r'^recruitment/findme/$', views.findme),
    url(r'^film/', views.movie_list, name="movie"),
    url(r'^deletefile/$', views.deletefile),
    url(r'^ajfileupload/$', views.ajupload_file),
    url(r'^filecheck/$', views.filecheck),
    url(r'^list/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.blog_time),
    url(r'^jiadmin/', views.JiaAdmin.as_view()),
    url(r'^resume/', views.Resume.as_view()),
    url(r'^collect/$', views.collect),
    url(r'^comments/(?P<article_id>[0-9]+)$', views.comments),
    url(r'^rss/$', views.RssFeed(), name='rss'),
    url(r'^searchfile/$', views.search_file),
    url(r'^getallarticle/$', views.get_article_all),
    url(r'^getsinglearticle/(?P<article_id>[0-9]+)/$', views.get_article_single),
    url(r'^single-article/(?P<rand_id>[A-Za-z0-9]+)/$', views.single_article),
    url(r'^getallcategory/$', views.get_categroy_all),
    url(r'^getcategoryarticles/(.+)/$', views.get_article_category),
    url(r'^gettagarticles/(.+)/$', views.get_article_tag),
    url(r'^new/search/$', views.BlogSearch.as_view()),
    url(r'^archive/$', views.BlogPostArchive.as_view()),
    url(r'^new/index/$', views.Index.as_view()),
    url(r'^post/(?P<article_id>[0-9]+)/(?P<slug>[-\w]+)/$', views.BlogPost.as_view()),
    url(r'^upload_file_springboot/$', views.upload_facepic_springboot),
    url(r'^sign_in/$', views.sign_in),
    url(r'^getlovefzytodo/$', views.GetLoveFZYToDoList.as_view()),
    url(r'^getlovefzydown/$', views.GetLoveFZYDownList.as_view()),
    url(r'^postlovefzy/$', views.PostLoveFZYInfo.as_view()),
    url(r'^getlovefzytimeline/$', views.GetLoveFZYTimeline.as_view()),
    url(r'^tags/$', views.show_tags),
    url(r'^api/upload/resumes/$', views.upload_resumes),
    url(r'^api/edit/article/(?P<rand_id>[A-Za-z0-9]+)/$', views.edit_article),
    # url(r'^convert/$', views.convert),
]
