from django.conf.urls import url
from blogproject import views

app_name = 'blogproject'


urlpatterns = [
    url(r'^post/(?P<article_id>[0-9]+)/(?P<url_slug>[-\w]+)/$', views.post_detail, name='post'),
    url(r'^auth/$', views.check_auth, name='auth'),
    url(r'^single-article/(?P<rand_id>[A-Za-z0-9]+)/$', views.single_article),
    url(r'^all-articles/$', views.get_articles_all),
    url(r'^single-article/(?P<rand_id>[A-Za-z0-9]+)/summary$', views.get_article_summary),
]
