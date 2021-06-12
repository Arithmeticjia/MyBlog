from django.conf.urls import url, include
from django.urls import path
from comment import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

app_name = 'comment'

urlpatterns = [
    # 已有代码，处理一级回复
    path('post-comment/<int:article_id>', views.post_comment, name='post_comment'),
    # 新增代码，处理二级回复
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply'),
    path('get-comment/<int:rand_id>', views.get_comment, name='comment')
]