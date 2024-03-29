import markdown
import re
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from text_summarization.summary import *
from django.views import View
from django.views.decorators.http import require_http_methods
from markdown.extensions.toc import TocExtension, slugify
from django.contrib.auth.decorators import login_required
from blog.models import SocialAuthUsersocialauth, Userip
from blogproject.models import Post, Category, User, Tag
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
        except Exception as e:
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


class PostArchiveView(View):

    def get(self, request):

        try:
            post_list = Post.objects.filter(status='published').order_by("-created_time")
            paginator = Paginator(post_list, 16)  # 分页，每页10条数据
            page = request.GET.get('page')
            try:
                contacts = paginator.page(page)  # contacts为Page对象！
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                contacts = paginator.page(paginator.num_pages)
            category_name_list = Category.objects.all()
            tag_name_list = Tag.objects.all()
            shanshajia = User.objects.get(username='shanshajia')
            year_month = set()  # 设置集合，无重复元素
            for a in post_list:
                year_month.add((a.timestamp.year, a.timestamp.month))  # 把每篇文章的年、月以元组形式添加到集合中
            counter = {}.fromkeys(year_month, 0)  # 以元组作为key，初始化字典
            for a in post_list:
                counter[(a.timestamp.year, a.timestamp.month)] += 1  # 按年月统计文章数目
            year_month_number = []  # 初始化列表
            for key in counter:
                year_month_number.append([key[0], key[1], counter[key]])  # 把字典转化为（年，月，数目）元组为元素的列表
            year_month_number.sort(reverse=True)  # 排序
            context = {
                'blog_list': post_list,
                'blog_list_views': blog_list_views,
                'blog_list_comments': blog_list_comments,
                'tags': tag_name_list,
                'contacts': contacts,
                'blog_list_greats': blog_list_greats,
                'categorys': category_name_list,
                'blog_list_three': blog_list_news,
                'shanshajia': shanshajia,
                'year_month_number': year_month_number,
                'oauth2_from': oauth2_from
            }
        except Exception as e:
            return render(request, '404.html')

        return render(request, 'blogproject/single.html', context=context)


class PostDetailView(View):

    def get(self, request, article_id, url_slug):

        try:
            post = get_object_or_404(Post, id=article_id)
            if post.url_slug != url_slug:
                return render(request, '404.html')
        except Exception as e:
            return render(request, '404.html')
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
            'toc': md.toc,
        }
        return render(request, 'blogproject/single.html', context=context)


@require_http_methods(["GET"])
def single_article(request, rand_id):
    # 记录访问ip和每个ip的次数
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip
    ip_exist = Userip.objects.filter(ip=str(client_ip))
    response = {}
    next_article_title = ""
    prev_article_title = ""
    next_article_id = 0
    prev_article_id = 0
    try:
        article = Post.objects.get(status=1, rand_id=rand_id)
        article_id = article.id
        if ip_exist:
            article.increase_views()
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


@require_http_methods(["GET"])
def get_articles_all(request):
    response = {}
    try:
        articles = Post.objects.filter(status=1).order_by("id")
        response['list'] = json.loads(
            core_serializers.serialize("json", articles, use_natural_foreign_keys=True, ensure_ascii=False))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@require_http_methods(["GET"])
def get_article_summary(request, rand_id):
    response = {}
    try:
        stop_word = []
        with open('text_summarization/stopWordList.txt', 'r') as f:
            for line in f.readlines():
                stop_word.append(line.strip())
        content = Post.objects.get(status=1, rand_id=rand_id).content
        summary = get_summary(content, stop_word, strip_tags(content), topK_ratio=0.3)
        response['summary'] = summary
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return HttpResponse(json.dumps(response, ensure_ascii=False))