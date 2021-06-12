import markdown
import re
import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.http import require_http_methods
from markdown.extensions.toc import TocExtension, slugify
from django.contrib.auth.decorators import login_required
from blog.models import SocialAuthUsersocialauth
from blogproject.models import Post, Category, User
from django.shortcuts import HttpResponse, render, redirect
from comment.models import Comment
from django.core import serializers as core_serializers
from rest_framework import serializers, viewsets


# Create your views here.

def post_detail_test(request, article_id, url_slug):
    pass


@login_required()
def check_auth(request):
    return HttpResponse("ok")


def get_oauth2_from(name):
    oauth2_from = ''

    if name:
        d_user_id = User.objects.get(username=name).id
        try:
            oauth2login = SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            oauth2_from = oauth2login.provider
        except:
            oauth2_from = 'Django'

    return oauth2_from


def post_detail(request, article_id, url_slug):
    try:
        post = get_object_or_404(Post, id=article_id)
        post.increase_views()
        if post.url_slug != url_slug:
            return render(request, '404.html')
    except Exception as e:
        return render(request, '404.html')
    likes = post.likes
    category_id = post.category.id
    tag_name = post.tags.values('name')
    category = get_object_or_404(Category, id=category_id)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify)
    ])
    post.content = md.convert(post.content)
    comments = Comment.objects.filter(post=article_id)
    context = {
        'post': post,
        'category': category,
        'tag': tag_name,
        'likes': likes,
        'toc': md.toc,
        'comments': comments,
        'oauth2_from': get_oauth2_from(request.user.username)

    }
    return render(request, 'blogproject/single.html', context=context)


class PostDetailView(View):

    def get(self, request, article_id, url_slug):

        try:
            post = get_object_or_404(Post, id=article_id)
            if post.url_slug != url_slug:
                return render(request, '404.html')
        except Exception as e:
            return render(request, '404.html')
        likes = post.likes
        category_id = post.category.id
        tag_name = post.tags.values('name')
        category = get_object_or_404(Category, id=category_id)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        post.content = md.convert(post.content)
        context = {
            'post': post,
            'category': category,
            'tag': tag_name,
            'likes': likes,
            'toc': md.toc,
        }
        return render(request, 'blogproject/single.html', context=context)


@require_http_methods(["GET"])
def single_article(request, rand_id):
    response = {}
    next_article_title = ""
    prev_article_title = ""
    next_article_id = 0
    prev_article_id = 0
    try:
        article_id = Post.objects.get(status=1, rand_id=rand_id).id
        article = Post.objects.filter(status=1).filter(rand_id=rand_id)
        try:
            prev_article_id = Post.objects.filter(id__lt=article_id, status=1).last().id
            prev_article_title = Post.objects.get(id=prev_article_id).title
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1
        try:
            next_article_id = Post.objects.filter(id__gt=article_id, status=1).first().id
            next_article_title = Post.objects.get(id=next_article_id).title
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1
        single_article = get_object_or_404(Post, id=article_id, status=1)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        single_article.content = md.convert(single_article.content)
        n = single_article.content.count('<div class="codehilite">', 0, len(single_article.content))
        for i in range(n):
            single_article.content = re.sub(r'<span></span>',
                                            '&nbsp;&nbsp;<button id="ecodecopy" ref="copy" style="'
                                            'background-color: #909399;border: none;cursor: pointer;'
                                            'color: white;'
                                            'padding: 6px 6px;'
                                            'text-align: center;'
                                            'text-decoration: none;'
                                            'display: inline-block;'
                                            'float:right;'
                                            'font-size: 12px" class="copy_btn" '
                                            'data-clipboard-action="copy" '
                                            'data-clipboard-target="#code{}"'
                                            'onclick="copyText()">复制</button> '
                                            '<div style="clear:both"></div>'
                                            '<div class="codehilite" id="code{}">'.format(i, i), single_article.content,
                                            1)
        single_article.content = single_article.content.replace("/media", "https://www.guanacossj.com/media")
        response['list'] = json.loads(
            core_serializers.serialize("json", article, use_natural_foreign_keys=True, ensure_ascii=False))
        response['msg'] = 'success'
        response['markdown'] = single_article.content
        response['error_num'] = 0
        response['prev_article_title'] = prev_article_title
        response['next_article_title'] = next_article_title
        response['prev_article_id'] = prev_article_id
        response['next_article_id'] = next_article_id
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return HttpResponse(json.dumps(response, ensure_ascii=False))
