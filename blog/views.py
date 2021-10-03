from django.shortcuts import render
from django.core import serializers as core_serializers
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db import models
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.syndication.views import Feed
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.views import View
from django.shortcuts import render_to_response, redirect, get_object_or_404, reverse, HttpResponseRedirect
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.core.mail import send_mail
from django.db.models import Q, IntegerField, CharField, DateTimeField
from django.views.decorators.http import require_POST
from django.db.models import Count
import re
from drf_haystack.serializers import HaystackSerializerMixin
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.views import APIView
from blog.models import Articles, Message, Tag, Category, Note, Comment, BlogUser, VisitNumber, Recruitment, \
    Recruinfo, Movie, JiaFile, Jia, BlogRole, Paper, Graduation, Honour, Teacher, Project, Version, BlogUserCollect, \
    SocialAuthUsersocialauth, AuthUser, Hits, LoveFZY
from blogproject.models import User
from django.contrib.auth import logout
import time
import os
from .forms import RegisterForm
import psutil
import datetime
import markdown
from markdown.extensions.toc import TocExtension
from blog.forms import CommentForm, MessageForm, UserForm, ArticleForm
from blog import models
from blog.forms import UploadFileForm
from functools import wraps
from .visit_info import change_info
import subprocess
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, viewsets
import json
from haystack.views import SearchView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import mixins
from collections import Counter


# Create your views here.
class BlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = [
            'id',
            'name',
        ]


# 列表序列化器
class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    authorname = UserSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Articles
        fields = [
            'id',
            'title',
            'body',
            'timestamp',
            'tags',
            'category',
            'authorname',
            'views',
        ]


# 详情序列化器
class PostRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    authorname = UserSerializer()
    tags = TagSerializer()
    body_html = serializers.CharField()

    class Meta:
        model = Articles
        fields = [
            "id",
            "title",
            "body",
            "body_html",
            "timestamp",
            "views",
            "category",
            "authorname",
            "tags",
        ]


class ArticlesSerializers(serializers.ModelSerializer):
    authorname = serializers.CharField(source='authorname.name')
    category = serializers.CharField(source='category.name')
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        # 指定的模型类
        model = Articles
        # 需要序列化的属性
        fields = [
            'id',
            'title',
            'body',
            'timestamp',
            'authorname',
            'views',
            'tags',
            'category'
        ]


class GetArticleInfo(viewsets.ModelViewSet):
    queryset = Articles.objects.all().order_by('-id')
    serializer_class = ArticlesSerializers


# 首页文章列表
class IndexPostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Articles.objects.all()
    pagination_class = BlogPagination
    permission_classes = [AllowAny]


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Articles.objects.all()
    permission_classes = [AllowAny]

    serializer_class_table = {
        'list': PostListSerializer,
        'retrieve': PostRetrieveSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class_table.get(
            self.action
        )


class Yun(View):
    def get(self, request):
        # name = Teacher.objects.get(name='李云').name
        # brief = Teacher.objects.get(name='李云').brief
        # office_address = Teacher.objects.get(name='李云').office_address
        liyun = Teacher.objects.get(name='李云')
        honour = Honour.objects.all()
        paper = Paper.objects.all()
        project = Project.objects.all()
        graduation = Graduation.objects.all()
        context = {
            # "name":name,
            # "brief":brief,
            # "office_address":office_address
            "liyun": liyun,
            "honour": honour,
            "paper": paper,
            "graduation": graduation,
            "project": project
        }
        return render(request, 'yunindex.html', context=context)


def index(request):
    change_info(request)
    return redirect('/blog/index/')


def admininndex(request):
    return render(request, 'adminindex.html')


def admincharts(request):
    return render(request, 'chart-morris.html')


class Resume(View):
    def get(self, request):
        # name = Jia.objects.get(name=)
        return render(request, 'resume.html')


class ArticleHaystackSerializer(HaystackSerializerMixin, PostListSerializer):
    class Meta(PostListSerializer.Meta):
        search_fields = ["text"]


class PostSearchView(HaystackViewSet):
    index_models = [Articles]
    serializer_class = ArticleHaystackSerializer


class MySearchView(SearchView):
    # 重载extra_context来添加额外的context内容
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        categorys = Category.objects.all()
        blog_list_greats = Articles.objects.filter(status="有效").order_by('-greats')[0:10]
        blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
        tags = Tag.objects.all()
        jia = Jia.objects.get(id=1)
        try:
            version = Version.objects.filter(version_time=datetime.datetime.now().strftime('%Y-%m-%d')).values(
                'version_content')
            versions = [item[key] for item in version for key in item][0].split(";")
        except IndexError as err:
            version = Version.objects.order_by('-version_time')[0:1].values('version_content')
            # all()[0:1].values('version_content')
            versions = [item[key] for item in version for key in item][0].split(";")
        context['categorys'] = categorys
        context['blog_list_greats'] = blog_list_greats
        context['blog_list_comments'] = blog_list_comments
        context['tags'] = tags
        context['versions'] = versions
        context['jia'] = jia

        return context


@csrf_exempt
def cancelcollect(request, article_id, slug):
    if request.method == "POST":
        blog_id = request.POST.get('article_id')
        name = request.session.get('user_name')
        name_id = str(BlogUser.objects.get(name=name).id)
        thisarticle = get_object_or_404(Articles, id=blog_id)
        # thisarticle.increase_views()
        data = {}

        if BlogUserCollect.objects.filter(blogid=blog_id, userid=name_id).count() >= 1:
            try:
                collect_obj = BlogUserCollect.objects.get(blogid=blog_id, userid=name_id)
                collect_obj.delete()
                data["result"] = "success"
            except Exception as e:
                data["result"] = "fail"
        else:
            data["result"] = "fail"
        return HttpResponse(json.dumps(data), content_type='application/json')


def check_admin(f):
    @wraps(f)
    def inner(request, *arg, **kwargs):
        cursor = connection.cursor()
        cursor.execute('select t.name from JiaBlog_bloguser t')
        raw_list = cursor.fetchall()
        cursor.close()  # 关闭游标
        # admins = BlogUser.objects.filter(role=BlogRole.objects.get(name='Admin')).values('name')
        admins = [item[key] for item in BlogUser.objects.filter(role=BlogRole.objects.get(name='Admin')).values('name')
                  for key in item]
        if request.session.get('user_name') in admins:
            return f(request, *arg, **kwargs)
        else:
            return redirect('/blog/login/')

    return inner


@method_decorator(check_admin, name='dispatch')
class JiaAdmin(View):

    def get(self, request):
        try:
            blog_users = BlogUser.objects.filter(status='有效')
            context = {
                'blog_users': blog_users,
            }
            return render(request, 'jiaadmin.html', context=context)
        except:
            return render(request, '404.html')

    def post(self, request):
        return render(request, 'jiaadmin.html')


def blog_time(request, year, month):
    change_info(request)
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    blog_lists = Articles.objects.filter(timestamp__year=year, timestamp__month=month, status="有效").order_by(
        '-timestamp')
    paginator = Paginator(blog_lists, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    comments = Comment.objects.count()
    tags = Tag.objects.all()
    count = Articles.objects.count()
    categorys = Category.objects.all()
    jia = Jia.objects.get(id=1)
    articles = Articles.objects.all().filter(status="有效")
    year_month = set()  # 设置集合，无重复元素
    for a in articles:
        year_month.add((a.timestamp.year, a.timestamp.month))  # 把每篇文章的年、月以元组形式添加到集合中
    counter = {}.fromkeys(year_month, 0)  # 以元组作为key，初始化字典
    for a in articles:
        counter[(a.timestamp.year, a.timestamp.month)] += 1  # 按年月统计文章数目
    year_month_number = []  # 初始化列表
    for key in counter:
        year_month_number.append([key[0], key[1], counter[key]])  # 把字典转化为（年，月，数目）元组为元素的列表
    year_month_number.sort(reverse=True)  # 排序
    this_year_month = [year + '.' + month]
    context = {
        'tags': tags,
        'contacts': contacts,
        'comments': comments,
        'categorys': categorys,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'jia': jia,
        'year_month_number': year_month_number,
        'this_year_month': this_year_month,
    }
    return render(request, 'blog/archive.html', context=context)


def check_login(f):
    @wraps(f)
    def inner(request, *arg, **kwargs):
        next_url = request.path_info
        if request.session.get('is_login') == True:
            return f(request, *arg, **kwargs)
        else:
            return redirect('/blog/login/?next=%s' % next_url)

    return inner


def login_view(request):
    # 当前端点击登录按钮时，提交数据到后端，进入该POST方法
    if request.method == "POST":
        # 获取用户名和密码
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 在前端传回时也将跳转链接传回来
        next_url = request.POST.get("next_url")
        # 对用户进行验证
        try:
            user = models.BlogUser.objects.get(name=username)
            if user.status == 'active' or user.status == '有效':
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    # 如果跳转链接不为空并且跳转页面不是登出页面，则登录成功后跳转，否则直接进入主页
                    if next_url and next_url != "/blog/logout/":
                        response = redirect(next_url)
                    else:
                        response = redirect("/blog/index/")
                    return response
                else:
                    message = "密码不正确！"
            # 若用户名或密码失败,则将提示语与跳转链接继续传递到前端
            else:
                message = "用户状态信息异常，请联系管理员(18351922995)! "

        except:
            message = "用户不存在！"
        return render(request, 'blog/login.html', locals())
    else:
        next_url = request.GET.get("next", '')
        return render(request, "blog/login.html", {'next_url': next_url}, locals())


def register_view(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/blog/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            # sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'blog/register.html', locals())
            else:
                same_name_user = models.BlogUser.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'blog/register.html', locals())
                same_email_user = models.BlogUser.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'blog/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.BlogUser.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = '男'
                new_user.userpic = 'userpic/img11.jpg'
                new_role = BlogRole.objects.get(name='Common')
                new_user.save()
                new_user = BlogUser.objects.get(name=username)
                new_user.role.add(new_role)
                return render(request, 'blog/login.html', locals())
    register_form = RegisterForm()
    return render(request, 'blog/register.html', locals())


class LogoutView(View):

    def get(self, request):
        logout(request)
        if not request.session.get('is_login', None):
            # 如果本来就未登录，也就没有登出一说
            return redirect("/blog/index/")
        # request.session.flush()
        # 或者使用下面的方法
        # logout(request)
        del request.session['is_login']
        del request.session['user_id']
        del request.session['user_name']
        del request.session['user_role']
        return redirect("/blog/login/")


def query_blog_lists():
    blog_lists = Articles.objects.filter(status="有效").order_by("-timestamp")[0:10]  # 获取所有数据
    return blog_lists


def query_blog_list_head():
    blog_list_head = Articles.objects.filter(status="有效").filter(istop=1).order_by("-timestamp")[0:5]
    return blog_list_head


# @cache_page(60 * 15)
def blog_index(request):
    # post = request.get_post(Articles, pk=pk)
    change_info(request)
    oauth2_from = ''
    if request.user.username:
        name = request.user.username
        d_user_id = User.objects.get(username=name).id
        try:
            #            SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            oauth2login = SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            #            oauth2_info = oauth2login.extra_data
            oauth2_from = oauth2login.provider
        #            user_dict = json.loads(oauth2_info)
        #            oauth2_name = user_dict['login']
        except:
            # oauth2_name = ' '
            oauth2_from = 'Django'
    blog_lists = Articles.objects.filter(status="有效").order_by("-timestamp")[0:10]  # 获取所有数据
    blog_list_head = Articles.objects.filter(status="有效").filter(istop=1).order_by("-timestamp")[0:5]  # 获取5 头部的5个
    blog_list_up = Articles.objects.filter(status="有效").filter(istop=2).order_by("-timestamp")[0:4]  # 获取2，上面的4个
    blog_list_middle = Articles.objects.filter(status="有效").order_by('-comments')[0:2]  # 获取2，中间那两个
    blog_list_down = Articles.objects.filter(status="有效").order_by('-greats')[0:2]  # 获取2，下面那两个
    blog_list_news = Articles.objects.filter(status="有效").order_by("-timestamp")[0:10]  # 获取3 recent posts
    blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:10]  # 点击排行
    blog_list_hots = Articles.objects.filter(status="有效").order_by('-views')[0:4]  # 点击排行
    blog_list_greats = Articles.objects.filter(status="有效").order_by('-greats')[0:10]  # 猜你喜欢
    blog_list_comments = Articles.objects.filter(status="有效").order_by('-comments')[0:10]  # 博主推荐
    blog_list_large = Articles.objects.filter(status="有效").order_by('-timestamp')[0:1]  # 获取1，最大那个
    articles = Articles.objects.all().filter(status="有效")
    year_month = set()  # 设置集合，无重复元素
    for a in articles:
        year_month.add((a.timestamp.year, a.timestamp.month))  # 把每篇文章的年、月以元组形式添加到集合中
    counter = {}.fromkeys(year_month, 0)  # 以元组作为key，初始化字典
    for a in articles:
        counter[(a.timestamp.year, a.timestamp.month)] += 1  # 按年月统计文章数目
    year_month_number = []  # 初始化列表
    for key in counter:
        year_month_number.append([key[0], key[1], counter[key]])  # 把字典转化为（年，月，数目）元组为元素的列表
    year_month_number.sort(reverse=True)  # 排序
    tags = Tag.objects.all()
    count = Articles.objects.count()
    categorys = Category.objects.all()
    catcharts = {}
    for cats in categorys:
        catnums = Articles.objects.filter(category=cats.id).filter(status='有效').count()
        catcharts[cats.name] = catnums
    maxmap = max(catcharts.values())
    minmap = min(catcharts.values())
    allvisit = VisitNumber.objects.first()
    jia = Jia.objects.get(id=1)
    try:
        version = models.Version.objects.filter(version_time=datetime.datetime.now().strftime('%Y-%m-%d')).values(
            'version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    except IndexError as err:
        print("error", err)
        version = models.Version.objects.order_by('-version_time')[0:1].values('version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    '''else:
        version = models.Version.objects.all()[0:1].values('version_content')
        versions = [item[key] for item in version for key in item][0].split(";")'''
    context = {
        'blog_list': blog_lists,
        'blog_list_views': blog_list_views,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'categorys': categorys,
        'count': count,
        'blog_list_five': blog_list_head,
        'blog_list_up': blog_list_up,
        'blog_list_middel': blog_list_middle,
        'blog_list_down': blog_list_down,
        'blog_list_three': blog_list_news,
        'blog_list_hots': blog_list_hots,
        'blog_list_large': blog_list_large,
        'max': maxmap,
        'min': minmap,
        'versions': versions,
        'allvisit': allvisit,
        'catcharts': catcharts,
        'jia': jia,
        'year_month_number': year_month_number,
        # 'oauth2':oauth2_name,
        'oauth2_from': oauth2_from
    }
    return render(request, 'blog/index.html', context=context)


def comments(request, article_id):
    thisarticle = get_object_or_404(Articles, id=article_id, status='有效')
    comment_list = thisarticle.comment_set.all()
    context = {
        'comment_list': comment_list
    }
    return render(request, 'comment.html', context=context)


def make_blog_user(hits):
    tmp = []
    for i in hits:
        tmp.append(i.userid)
    users = list(set(tmp))
    hitsdict = {}
    for j in tmp:
        hitsdict.update({'user%d' % int(j): []})
    for i in hits:
        print(model_to_dict(i))
    print(hitsdict)


def blog_info(request, article_id, slug):
    change_info(request)
    login_name = request.session.get('user_name')
    oauth2_from = ''
    if request.user.username:
        name = request.user.username
        d_user_id = User.objects.get(username=name).id
        try:
            oauth2login = SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            #            oauth2_info = oauth2login.extra_data
            oauth2_from = oauth2login.provider
        #            user_dict = json.loads(oauth2_info)
        #            oauth2_name = user_dict['login']
        except:
            # oauth2_name = ' '
            oauth2_from = 'Django'
    # noinspection PyBroadException
    try:
        thisarticle = get_object_or_404(Articles, id=article_id, status='有效')
        if thisarticle.url_slug != slug:
            return render(request, '404.html')
        thisarticle.increase_views()
    except Exception as e:
        return render(request, '404.html')
    try:
        if login_name is not None:
            hit = Hits.objects.get(userid=int(BlogUser.objects.get(name=login_name).id), blogid=int(article_id))
            hit.hitnum = hit.hitnum + 1
            hit.save()
        else:
            pass
    except:
        obj = Hits(userid=int(BlogUser.objects.get(name=login_name).id), blogid=int(article_id), hitnum=1)
        obj.save()
    greats = thisarticle.greats
    comment_list = thisarticle.comment_set.all()
    blog_list_all = Articles.objects.filter(status="有效").order_by("-views")[0:10]
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    blog_list_news = Articles.objects.filter(status="有效").order_by("-timestamp")[0:10]  # 获取10 recent posts
    category_id = thisarticle.category.id
    tag_name = thisarticle.tags.values('name')
    tag_name = [item[key] for item in tag_name for key in item]
    tag = (" ".join(tag_name)).split(" ")
    category = get_object_or_404(Category, id=category_id)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify)
    ])
    md_body = thisarticle.body
    thisarticle.body = markdown.markdown(thisarticle.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify)
    ])
    md_body = md.convert(md_body)
    n = thisarticle.body.count('<div class="codehilite">', 0, len(thisarticle.body))
    for i in range(n):
        thisarticle.body = re.sub(r'<span></span>',
                                  '&nbsp;&nbsp;<button id="ecodecopy" style="'
                                  'background-color: #555555;border: none;'
                                  'color: white;'
                                  'padding: 6px 6px;'
                                  'text-align: center;'
                                  'text-decoration: none;'
                                  'display: inline-block;'
                                  'float:right;'
                                  'font-size: 12px" class="copybtn" '
                                  'data-clipboard-action="copy" '
                                  'data-clipboard-target="#code{}">copy</button> '
                                  '<div class="codehilite" id="code{}">'.format(i, i), thisarticle.body, 1)
    comment_list = thisarticle.comment_set.all()
    # thisarticle.body = md.convert(thisarticle.body)
    categorys = Category.objects.all()
    jia = Jia.objects.get(id=1)
    related_blog = Articles.objects.filter(status="有效").filter(category=thisarticle.category).filter(~Q(id=article_id))[
                   0:2]
    try:
        version = models.Version.objects.filter(version_time=datetime.datetime.now().strftime('%Y-%m-%d')).values(
            'version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    except IndexError as err:
        print("error", err)
        version = models.Version.objects.order_by('-version_time')[0:1].values('version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    articles = Articles.objects.all().filter(status="有效")
    year_month = set()  # 设置集合，无重复元素
    for a in articles:
        year_month.add((a.timestamp.year, a.timestamp.month))  # 把每篇文章的年、月以元组形式添加到集合中
    counter = {}.fromkeys(year_month, 0)  # 以元组作为key，初始化字典
    for a in articles:
        counter[(a.timestamp.year, a.timestamp.month)] += 1  # 按年月统计文章数目
    year_month_number = []  # 初始化列表
    for key in counter:
        year_month_number.append([key[0], key[1], counter[key]])  # 把字典转化为（年，月，数目）元组为元素的列表
    year_month_number.sort(reverse=True)  # 排序
    if BlogUserCollect.objects.filter(blogid=article_id).count() >= 1:
        collect_flag = 1
    else:
        collect_flag = 0
    context = {
        'blog_list': thisarticle,
        'blog_list_all': blog_list_all,
        'comment_list': comment_list,
        'category': category,
        'tag': tag_name,
        'blog_list_three': blog_list_news,
        'tags': tag,
        'greats': greats,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'categorys': categorys,
        'related_blog': related_blog,
        'versions': versions,
        'jia': jia,
        'year_month_number': year_month_number,
        'toc': md.toc,
        'collect_flag': collect_flag,
        'oauth2_from': oauth2_from

    }

    return render(request, 'blog/single.html', context=context)


def blog_list(request):
    change_info(request)
    oauth2_from = ''
    if request.user.username:
        name = request.user.username
        d_user_id = User.objects.get(username=name).id
        try:
            #            SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            oauth2login = SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            #            oauth2_info = oauth2login.extra_data
            oauth2_from = oauth2login.provider
        #            user_dict = json.loads(oauth2_info)
        #            oauth2_name = user_dict['login']
        except:
            # oauth2_name = ' '
            oauth2_from = 'Django'
    # post = request.get_post(Articles, pk=pk)
    blog_list = Articles.objects.filter(status="有效").order_by("-timestamp")  # 获取所有数据
    paginator = Paginator(blog_list, 16)  # 分页，每页10条数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:10]
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    blog_list_news = Articles.objects.filter(status="有效").order_by("-timestamp")[0:10]  # 获取10 recent posts
    comments = Comment.objects.count()
    tags = Tag.objects.all()
    categorys = Category.objects.all()
    jia = Jia.objects.get(id=1)
    try:
        version = models.Version.objects.filter(version_time=datetime.datetime.now().strftime('%Y-%m-%d')).values(
            'version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    except IndexError as err:
        print("error", err)
        version = models.Version.objects.order_by('-version_time')[0:1].values('version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    articles = Articles.objects.all().filter(status="有效")
    year_month = set()  # 设置集合，无重复元素
    for a in articles:
        year_month.add((a.timestamp.year, a.timestamp.month))  # 把每篇文章的年、月以元组形式添加到集合中
    counter = {}.fromkeys(year_month, 0)  # 以元组作为key，初始化字典
    for a in articles:
        counter[(a.timestamp.year, a.timestamp.month)] += 1  # 按年月统计文章数目
    year_month_number = []  # 初始化列表
    for key in counter:
        year_month_number.append([key[0], key[1], counter[key]])  # 把字典转化为（年，月，数目）元组为元素的列表
    year_month_number.sort(reverse=True)  # 排序
    context = {
        'blog_list': blog_list,
        'blog_list_views': blog_list_views,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'contacts': contacts,
        'blog_list_greats': blog_list_greats,
        'comments': comments,
        'categorys': categorys,
        'blog_list_three': blog_list_news,
        'versions': versions,
        'jia': jia,
        'year_month_number': year_month_number,
        'oauth2_from': oauth2_from
    }
    return render(request, 'blog/archive.html', context=context)


def sendemail(request):
    email_title = '邮件标题'
    email_body = '邮件内容'
    email = '1524126437@qq.com'  # 对方的邮箱
    send_mail(email_title, email_body, '1524126437@qq.com', [email])
    return render_to_response('myweather.html')


FILE_HOME_DIR = "./static/film"
MEDIA = [".mp4", ".qsv"]


def timeline(request):
    return render_to_response('oblog/newtimeline.html')


'''def greats(request,article_id):
    blogs = Articles.objects.count()  # 获取所有博客的总数
    thisarticle = get_object_or_404(Articles, id=article_id)
    thisarticle.increase_views()
    thisarticle.greats += 1
    thisarticle.save()
    greats = thisarticle.greats
    
    if int(article_id) == 1:
        leftarticle = '这已经是第一篇啦'
    else:
        leftarticle = get_object_or_404(Articles, id=str(int(article_id) - 1))
    if int(article_id) == blogs:
        rightarticle = '这已经是最后一篇啦'
    else:
        rightarticle = get_object_or_404(Articles, id=str(int(article_id) + 1))
    comment_list = thisarticle.comment_set.all()
    form = CommentForm()
    view = []
    count = Articles.objects.count()
    for ids in range(1, count + 1):
        article = get_object_or_404(Articles, id=str(ids))
        view.append(article.increase_views())
    maxview = int(view.index(max(view))) + 1
    maxarticle = Articles.objects.filter(id=str(maxview))
    blog_list_all = Articles.objects.order_by("-views")
    category_id = thisarticle.category.id
    tag_name = thisarticle.tags.values('name')
    tag_name = [item[key] for item in tag_name for key in item]
    tag = (" ".join(tag_name))
    category = get_object_or_404(Category, id=category_id)
    thisarticle.body = markdown.markdown(thisarticle.body, extensions=[
                                                                       'markdown.extensions.extra',
                                                                       'markdown.extensions.codehilite',
                                                                       'markdown.extensions.toc',
                                                                       ])
    context = {
                                                                           'maxview': maxarticle,
                                                                               'blog_list': thisarticle,
                                                                                   'blog_list_all': blog_list_all,
                                                                                       'form': form,
                                                                                           'comment_list': comment_list,
                                                                                               'right_blog_list': rightarticle,
                                                                                                   'left_blog_list': leftarticle,
                                                                                                       'category': category,
                                                                                                           'tag': tag_name,
                                                                                                               'tags': tag,
                                                                                                                   'greats': greats,
                                                                                                               }
    #return render(request, 'info.html', context=context)  # 返回info.html页面
    return redirect('/blog/article/%s' %(article_id))'''

'''def blog_category(request, blog_category):
    blog_list = Articles.objects.filter(category__name__exact=blog_category) # 获取所有数据
    paginator = Paginator(blog_list, 10)  # 分页，每页10条数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    
    blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:10]
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    comments = Comment.objects.count()
    tags = Tag.objects.all()
    count = Articles.objects.count()
    categorys = Category.objects.all()
    context = {
        'blog_list': blog_list,
        'blog_list_views': blog_list_views,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'contacts': contacts,
        'blog_list_greats': blog_list_greats,
        'comments': comments,
        'categorys':categorys,
        'blog_category':blog_category,
    }
    # print((maxarticle))
    return render(request, 'archive.html', context=context)'''


def greats(request):
    change_info(request)
    if request.method == "POST":
        id = request.POST.get('article_id')
        thisarticle = get_object_or_404(Articles, id=id)
        thisarticle.increase_views()
        thisarticle.greats += 1
        thisarticle.save()
        greats = {}
        greats["result"] = str(thisarticle.greats)
        return HttpResponse(json.dumps(greats), content_type='application/json')


def blog_category(request, blog_category):
    change_info(request)
    oauth2_from = ''
    if request.user.username:
        name = request.user.username
        d_user_id = User.objects.get(username=name).id
        try:
            #            SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            oauth2login = SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            #            oauth2_info = oauth2login.extra_data
            oauth2_from = oauth2login.provider
        #            user_dict = json.loads(oauth2_info)
        #            oauth2_name = user_dict['login']
        except:
            # oauth2_name = ' '
            oauth2_from = 'Django'
    cate = get_object_or_404(Category, name=blog_category)
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    blog_lists = Articles.objects.filter(category=cate).filter(status="有效").order_by('id')
    blog_list_news = Articles.objects.filter(status="有效").order_by("-timestamp")[0:10]  # 获取10 recent posts
    paginator = Paginator(blog_lists, 10)  # 分页，每页10条数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    comments = Comment.objects.count()
    tags = Tag.objects.all()
    count = Articles.objects.count()
    categorys = Category.objects.all()
    jia = Jia.objects.get(id=1)
    articles = Articles.objects.all().filter(status="有效")
    year_month = set()  # 设置集合，无重复元素
    for a in articles:
        year_month.add((a.timestamp.year, a.timestamp.month))  # 把每篇文章的年、月以元组形式添加到集合中
    counter = {}.fromkeys(year_month, 0)  # 以元组作为key，初始化字典
    for a in articles:
        counter[(a.timestamp.year, a.timestamp.month)] += 1  # 按年月统计文章数目
    year_month_number = []  # 初始化列表
    for key in counter:
        year_month_number.append([key[0], key[1], counter[key]])  # 把字典转化为（年，月，数目）元组为元素的列表
    year_month_number.sort(reverse=True)  # 排序
    context = {
        'tags': tags,
        'contacts': contacts,
        'comments': comments,
        'categorys': categorys,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'blog_category': blog_category,
        'blog_list_three': blog_list_news,
        'jia': jia,
        'year_month_number': year_month_number,
        'oauth2_from': oauth2_from
    }
    return render(request, 'blog/archive.html', context=context)


'''def comment_view(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        message = "请检查填写的内容！"
        data = {}
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = article
            comment.save()
            Articles.objects.update(comments=article.all_comments.count())
            thisarticle = get_object_or_404(Articles, id=article_id)
            comment_list = thisarticle.comment_set.all()
            data['status'] = 'Success'
            data['username'] = comment.name
            data['comment_time'] = comment.created_time.strftime('%Y-%m-%d %H:%M:%S')
            data['text'] = comment.text
            data['email'] = comment.email
        else:
            data['status'] = 'Error'
            data['message'] = "Error!"
        return HttpResponse(json.dumps(data), content_type='application/json')'''


def comment_view(request, article_id, cid):
    if request.method == 'POST':
        name = request.session.get('user_name')
        email = BlogUser.objects.get(name=name).email
        article = get_object_or_404(Articles, id=article_id)
        form = CommentForm(request.POST)
        commentered = BlogUser.objects.get(name=article.authorname)
        commenter = BlogUser.objects.get(name=name)
        print(form)
        data = {}
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = article_id
            comment.email = email
            comment.name = BlogUser.objects.get(name=name)
            print(comment.name, comment.email, comment.post_id, comment.text)
            if cid == 'no':
                comment.parentcomment = None
            else:
                comment.parentcomment_id = cid
            try:
                comment.save()
                # notify.send(
                #     commenter,               # 消息发送人
                #     recipient=commentered,      # 消息接收人
                #     verb='回复了你',
                #     target=article,
                #     action_object=comment,
                # )
                Articles.objects.update(comments=article.all_comments.count())
                data['status'] = 'Success'
                data['username'] = name
                data['comment_time'] = comment.created_time.strftime('%Y-%m-%d %H:%M:%S')
                data['text'] = comment.text
                data['email'] = comment.email
                userpic = [item[key] for item in BlogUser.objects.filter(name=name).values('userpic') for key in item][
                    0]
                data['userpic'] = userpic
                comments = Comment.objects.filter(post_id=article_id).count()
                data['comments'] = comments
                print(comment.parentcomment)
                if comment.parentcomment == None:
                    data['pid'] = ''
                else:
                    data['pid'] = comment.parentcomment_id
                print('ooookkkk', data)
            except:
                data['status'] = 'Error'
                data['message'] = "Error!"
        else:
            data['status'] = 'Error'
            data['message'] = "Error!"
        # return redirect('/blog/article/%s' % (article_id))
        return HttpResponse(json.dumps(data), content_type='application/json')


def contact(request):
    change_info(request)
    oauth2_from = ''
    if request.user.username:
        name = request.user.username
        d_user_id = User.objects.get(username=name).id
        try:
            #            SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            oauth2login = SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            #            oauth2_info = oauth2login.extra_data
            oauth2_from = oauth2login.provider
        #            user_dict = json.loads(oauth2_info)
        #            oauth2_name = user_dict['login']
        except:
            # oauth2_name = ' '
            oauth2_from = 'Django'
    if request.method == 'GET':
        # 取出当前在models表中所有的留言信息 ,返回到前端
        allmessage = Message.objects.all()
        jia = Jia.objects.get(id=1)
        users = BlogUser.objects.all().filter(status='有效').count()
        articles = Articles.objects.all().filter(status='有效').count()
        visits = VisitNumber.objects.first()
        context = {
            "messages": allmessage,
            "jia": jia,
            "users": users,
            "articles": articles,
            "visits": visits,
            'oauth2_from': oauth2_from
        }
        return render(request, "blog/contact-us.html", context=context)
    return render_to_response('blog/contact-us.html')


def savemessage(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        data = {}
        if form.is_valid():
            message = form.save(commit=False)
            try:
                message.save()
            except Exception as e:
                data['status'] = '500'
            else:
                thismessage = Message.objects.get(id=message.id)  # 刚入库的留言
                usernames = models.BlogUser.objects.all().values('name')  # 用户表所有name
                usernames = [item[key] for item in usernames for key in item]
                if message.username in usernames:
                    thismessage.messpic = BlogUser.objects.get(name=thismessage.username).userpic.url
                    thismessage.save()
                    data["username"] = thismessage.username
                    data["title"] = thismessage.title
                    data["content"] = thismessage.content
                    data["email"] = thismessage.email
                    data['time'] = thismessage.publish.strftime("%Y-%m-%d %H:%M:%S")
                    data["phone"] = thismessage.phone
                    data["messpic"] = thismessage.messpic
                    email_title = '每一点进步离不开你的宝贵意见，由衷感谢你的支持~'
                    email_body = '已经收到你的宝贵意见，我们会持续改进。--From ArithmeticJia'
                    email = thismessage.email  # 对方的邮箱
                    try:
                        send_mail(email_title, email_body, '1524126437@qq.com', [email])
                    except Exception as e:
                        data['status'] = '500'
                        return HttpResponse(json.dumps(data), content_type='application/json')
                    return HttpResponse(json.dumps(data), content_type='application/json')
                else:
                    thismessage.messpic = '/static/blog/images/img56.jpg'
                    thismessage.save()
                    data["username"] = thismessage.username
                    data["title"] = thismessage.title
                    data["content"] = thismessage.content
                    data["email"] = thismessage.email
                    data['time'] = thismessage.publish.strftime("%Y-%m-%d %H:%M:%S")
                    data["phone"] = thismessage.phone
                    data["messpic"] = thismessage.messpic
                    email_title = '每一点进步离不开你的宝贵意见，由衷感谢你的支持~'
                    email_body = '已经收到你的宝贵意见，我们会持续改进。--From ArithmeticJia'
                    email = thismessage.email  # 对方的邮箱
                    # send_mail(email_title, email_body, '1524126437@qq.com', [email])
                    try:
                        send_mail(email_title, email_body, '1524126437@qq.com', [email])
                    except Exception as e:
                        data['status'] = '500'
                        return HttpResponse(json.dumps(data), content_type='application/json')
                    return HttpResponse(json.dumps(data), content_type='application/json')


# def upload_file(request):
#    if request.method == 'POST':
#        form = UploadFileForm(request.POST, request.FILES)
#        if form.is_valid():
#            print("ssss")
#            handle_uploaded_file(request.FILES['file'])
#            return HttpResponse("success")
#    else:
#        form = UploadFileForm()
#    return render(request, 'upload.html', {'form': form})
#
#
# def handle_uploaded_file(f):
#    with open('./blog/file/file.txt', 'wb+') as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)

def Jiafile(request):
    oauth2_from = ''
    if request.user.username:
        name = request.user.username
        d_user_id = User.objects.get(username=name).id
        try:
            #            SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            oauth2login = SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            #            oauth2_info = oauth2login.extra_data
            oauth2_from = oauth2login.provider
        #            user_dict = json.loads(oauth2_info)
        #            oauth2_name = user_dict['login']
        except:
            # oauth2_name = ' '
            oauth2_from = 'Django'
    file_name = []
    for filename in os.listdir(r'static/Jia_File'):
        file_name.append(filename)
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    tags = Tag.objects.all()
    categorys = Category.objects.all()
    jia = Jia.objects.get(id=1)
    jiafiles = JiaFile.objects.all().filter(file_status=1)
    try:
        version = models.Version.objects.filter(version_time=datetime.datetime.now().strftime('%Y-%m-%d')).values(
            'version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    except IndexError as err:
        version = models.Version.objects.order_by('-version_time')[0:1].values('version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    context = {
        'recruitmentinfo': recruitmentinfo,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'categorys': categorys,
        'file_name': file_name,
        'jiafiles': jiafiles,
        'versions': versions,
        'jia': jia,
        'oauth2_from': oauth2_from
    }
    return render(request, 'blog/upload.html', context=context)


@csrf_exempt
def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        form = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        # if not myFile:
        #     return HttpResponse("no files for upload!")
        file_obj = models.JiaFile(file_name=form.name, file_url='static/Jia_File/' + form.name, file_status=1)
        file_obj.save()
        destination = open(os.path.join("static/Jia_File", form.name), 'wb')  # 打开特定的文件进行二进制的写操作
        for chunk in form.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
    else:
        form = UploadFileForm()
    return redirect('/blog/file')


@check_login
def usereditor(request, article_id, slug):
    # article = Articles.objects.filter(id=article_id)
    article = get_object_or_404(Articles, id=article_id)
    article_user_id = article.authorname_id
    jia = Jia.objects.get(id=1)
    if request.session.get('user_id') == article_user_id:
        categorys = Category.objects.all()
        tags = Tag.objects.all()
        tag_name = article.tags.values('name')
        tag_name = [item[key] for item in tag_name for key in item]
        tag_name = (" ".join(tag_name)).split(" ")
        context = {
            "article": article,
            "categorys": categorys,
            "tags": tags,
            "tag_name": tag_name,
            "jia": jia,
        }
        return render(request, 'blog/usereditor.html', context)
    else:
        return render(request, '404.html')


@check_login
def mylist(request):
    change_info(request)
    oauth2_from = ''
    if request.user.username:
        name = request.user.username
        d_user_id = User.objects.get(username=name).id
        try:
            #            SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            oauth2login = SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            #            oauth2_info = oauth2login.extra_data
            oauth2_from = oauth2login.provider
        #            user_dict = json.loads(oauth2_info)
        #            oauth2_name = user_dict['login']
        except:
            # oauth2_name = ' '
            oauth2_from = 'Django'
    name = request.session.get('user_name')
    username = name
    blog_list = Articles.objects.filter(status="有效").filter(authorname__name__exact=username).order_by(
        "-timestamp")  # 获取所有数据
    paginator = Paginator(blog_list, 10)  # 分页，每页10条数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:10]
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    blog_list_news = Articles.objects.filter(status="有效").order_by("-timestamp")[0:10]  # 获取10 recent posts
    comments = Comment.objects.count()
    tags = Tag.objects.all()
    view = []
    count = Articles.objects.count()
    categorys = Category.objects.all()
    catcharts = {}
    for cats in categorys:
        catnums = Articles.objects.filter(category=cats.id).filter(status='有效').filter(
            authorname__name__exact=username).count()
        if catnums != 0:
            catcharts[cats.name] = catnums
        else:
            continue
    user = BlogUser.objects.get(name=name)
    mycategorys = Category.objects.filter(
        id__in=set([item[key] for item in blog_list.values('category') for key in item])).values('name')
    mycategorys = list([item[key] for item in mycategorys for key in item])
    django = Articles.objects.filter(category=1).filter(status='有效').filter(authorname__name__exact=username).count()
    python = Articles.objects.filter(category=2).filter(status='有效').filter(authorname__name__exact=username).count()
    leetcode = Articles.objects.filter(category=3).filter(status='有效').filter(authorname__name__exact=username).count()
    mysql = Articles.objects.filter(category=4).filter(status='有效').filter(authorname__name__exact=username).count()
    other = Articles.objects.filter(category=5).filter(status='有效').filter(authorname__name__exact=username).count()
    java = Articles.objects.filter(category=6).filter(status='有效').filter(authorname__name__exact=username).count()
    javascript = Articles.objects.filter(category=7).filter(status='有效').filter(
        authorname__name__exact=username).count()
    categorynum = [django, python, leetcode, mysql, other, java, javascript]
    categorydic = dict(zip(mycategorys, categorynum))
    try:
        version = models.Version.objects.filter(version_time=datetime.datetime.now().strftime('%Y-%m-%d')).values(
            'version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    except IndexError as err:
        print("error", err)
        version = models.Version.objects.order_by('-version_time')[0:1].values('version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    else:
        version = models.Version.objects.all()[0:1].values('version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    my_collects_obj = BlogUserCollect.objects.filter(userid=BlogUser.objects.get(name=username).id).values('blogid')
    my_collects = Articles.objects.filter(id__in=list([item[key] for item in my_collects_obj for key in item]))
    context = {
        'blog_list': blog_list,
        'blog_list_views': blog_list_views,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'contacts': contacts,
        'blog_list_greats': blog_list_greats,
        'blog_list_three': blog_list_news,
        'comments': comments,
        'categorys': categorys,
        'versions': versions,
        'user': user,
        'mycategorys': mycategorys,
        # 'mycategory':mycategory,
        'django': django,
        'python': python,
        'mysql': mysql,
        'leetcode': leetcode,
        'other': other,
        'java': java,
        'javascript': javascript,
        'categorydic': categorydic,
        'catcharts': catcharts,
        'my_collects': my_collects,
        'oauth2_from': oauth2_from
    }
    # print((maxarticle))
    return render(request, 'blog/editorlist.html', context=context)


@check_login
def mylist_para(request, article_status):
    change_info(request)
    name = request.session.get('user_name')
    username = name
    if article_status == 'active':
        blog_list = Articles.objects.filter(status="有效").filter(authorname__name__exact=username).order_by(
            "-timestamp")  # 获取所有数据
        paginator = Paginator(blog_list, 10)  # 分页，每页10条数据
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        categorys = Category.objects.all()
        blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:10]
        blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
        blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
        comments = Comment.objects.count()
        tags = Tag.objects.all()
        user = BlogUser.objects.get(name=name)
        catcharts = {}
        for cats in categorys:
            catnums = Articles.objects.filter(category=cats.id).filter(status='有效').filter(
                authorname__name__exact=username).count()
            if catnums != 0:
                catcharts[cats.name] = catnums
            else:
                continue
        mycategorys = Category.objects.filter(
            id__in=set([item[key] for item in blog_list.values('category') for key in item])).values('name')
        mycategorys = list([item[key] for item in mycategorys for key in item])
        try:
            version = models.Version.objects.filter(version_time=datetime.datetime.now().strftime('%Y-%m-%d')).values(
                'version_content')
            versions = [item[key] for item in version for key in item][0].split(";")
        except IndexError as err:
            version = models.Version.objects.all()[0:1].values('version_content')
            versions = [item[key] for item in version for key in item][0].split(";")
        else:
            version = models.Version.objects.all()[0:1].values('version_content')
            versions = [item[key] for item in version for key in item][0].split(";")
        my_collects_obj = BlogUserCollect.objects.filter(userid=BlogUser.objects.get(name=username).id).values('blogid')
        my_collects = Articles.objects.filter(id__in=list([item[key] for item in my_collects_obj for key in item]))
        context = {
            'blog_list': blog_list,
            'blog_list_views': blog_list_views,
            'blog_list_comments': blog_list_comments,
            'tags': tags,
            'contacts': contacts,
            'blog_list_greats': blog_list_greats,
            'comments': comments,
            'categorys': categorys,
            'versions': versions,
            'user': user,
            'mycategorys': mycategorys,
            'article_status': article_status,
            'catcharts': catcharts,
            'my_collects': my_collects
        }
    elif article_status == 'draft':
        blog_list = Articles.objects.filter(status="DRAFT").filter(authorname__name__exact=username).order_by(
            "-timestamp")  # 获取所有数据
        paginator = Paginator(blog_list, 10)  # 分页，每页10条数据
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        categorys = Category.objects.all()
        blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:10]
        blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
        blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
        comments = Comment.objects.count()
        tags = Tag.objects.all()
        user = BlogUser.objects.get(name=name)
        catcharts = {}
        for cats in categorys:
            catnums = Articles.objects.filter(category=cats.id).filter(status='DRAFT').filter(
                authorname__name__exact=username).count()
            if catnums != 0:
                catcharts[cats.name] = catnums
            else:
                continue
        mycategorys = Category.objects.filter(
            id__in=set([item[key] for item in blog_list.values('category') for key in item])).values('name')
        mycategorys = list([item[key] for item in mycategorys for key in item])
        try:
            version = models.Version.objects.filter(version_time=datetime.datetime.now().strftime('%Y-%m-%d')).values(
                'version_content')
            versions = [item[key] for item in version for key in item][0].split(";")
        except IndexError as err:
            version = models.Version.objects.all()[0:1].values('version_content')
            versions = [item[key] for item in version for key in item][0].split(";")
        else:
            version = models.Version.objects.all()[0:1].values('version_content')
            versions = [item[key] for item in version for key in item][0].split(";")
        my_collects_obj = BlogUserCollect.objects.filter(userid=BlogUser.objects.get(name=username).id).values('blogid')
        my_collects = Articles.objects.filter(id__in=list([item[key] for item in my_collects_obj for key in item]))
        context = {
            'blog_list': blog_list,
            'blog_list_views': blog_list_views,
            'blog_list_comments': blog_list_comments,
            'tags': tags,
            'contacts': contacts,
            'blog_list_greats': blog_list_greats,
            'comments': comments,
            'categorys': categorys,
            'versions': versions,
            'user': user,
            'mycategorys': mycategorys,
            'article_status': article_status,
            'catcharts': catcharts,
            'my_collects': my_collects
        }
    return render(request, 'blog/editorlist.html', context=context)


def article_save(request, article_id, slug):
    change_info(request)
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        category = request.POST.get('category')
        tags = request.POST.getlist('tags')
        newtags = Tag.objects.filter(name__in=tags)
        status = request.POST.get('status')
        tag_id = []
        for i in newtags:
            tag_id.append(i.id)
        pic = request.FILES.get('pic')
        try:
            article = Articles.objects.get(id=article_id)
            article.title = title
            article.body = body
            article.status = status
            article.category_id = Category.objects.get(name=category).id
            articlebodybrief = body.replace('```', '').replace('`', '')
            # if '```' in body[0:300]:
            #     pass
            # else:
            if len(articlebodybrief) >= 200:
                article.articlebodybrief = articlebodybrief[0:200]
            else:
                article.articlebodybrief = articlebodybrief
            if pic != None:
                article.pic = pic
                article.tags.set(tag_id)
                article.save()
                from PIL import Image
                print(article.pic.url)
                img = Image.open('.%s' % (article.pic.url))
                width, height = img.size
                w = int(width / 800)
                h = int(height / 450)
                if width >= 1600 and height >= 900:
                    cropped = img.resize((int(width / w), int(height / h)))
                    newwidth, newheight = cropped.size
                    lcropped = cropped.crop((newwidth / 2 - 400, newheight / 2 - 225, newwidth / 2 + 400,
                                             newheight / 2 + 225))  # (left, upper, right, lower)
                else:
                    lcropped = img.crop((width / 2 - 400, height / 2 - 225, width / 2 + 400, height / 2 + 225))
                lcropped.save('.%s' % (article.pic.url))
            # article.pic.url = article.pic.url
            else:
                article.tags.set(tag_id)
                article.save()
        except:
            messages = '编辑失败'
            return HttpResponse(messages)
        return redirect('/blog/mylist/')


def article_create(request):
    change_info(request)
    category = Category.objects.all()
    jia = Jia.objects.get(id=1)
    tags = Tag.objects.all()
    context = {
        'category': category,
        'tags': tags,
        'jia': jia,
    }
    return render(request, 'blog/usercreate.html', context)


def article_create_save(request):
    change_info(request)
    if request.method == 'POST':
        name = request.session.get('user_name')
        title = request.POST.get('title')
        body = request.POST.get('body')
        articlebodybrief = body.replace('```', '').replace('`', '')
        category = request.POST.get('category')
        category = Category.objects.get(name=category)
        tags = request.POST.getlist('tags')
        status = request.POST.get('status')
        pic = request.FILES.get('pic')
        newtags = Tag.objects.filter(name__in=tags)
        tag_id = []
        for i in newtags:
            tag_id.append(i.id)
        form = ArticleForm(request.POST)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.authorname = BlogUser.objects.get(name=name)
                post.greats = 0
                post.category_id = category.id
                post.body = body
                if len(articlebodybrief) >= 200:
                    post.articlebodybrief = articlebodybrief[0:200]
                else:
                    post.articlebodybrief = articlebodybrief
                post.comments = 0
                post.status = status
                post.pic = pic
                post.views = 0
                post.timestamp = timezone.now()
                post.save()
                post.tags.set(tag_id)
                post.save()
            except:
                messages = '创建失败'
                return HttpResponse(messages)
            post.pic = pic
            post.tags.set(tag_id)
            post.save()
            from PIL import Image
            img = Image.open('.%s' % (post.pic.url))
            width, height = img.size
            w = int(width / 800)
            h = int(height / 450)
            if width >= 1600 and height >= 900:
                cropped = img.resize((int(width / w), int(height / h)))
                newwidth, newheight = cropped.size
                lcropped = cropped.crop((newwidth / 2 - 400, newheight / 2 - 225, newwidth / 2 + 400,
                                         newheight / 2 + 225))  # (left, upper, right, lower)
            else:
                lcropped = img.crop((width / 2 - 400, height / 2 - 225, width / 2 + 400, height / 2 + 225))
            lcropped.save('.%s' % (post.pic.url))
        else:
            messages = '创建失败'
            return HttpResponse(messages)
        return redirect('/blog/mylist/')


@csrf_exempt
def article_delete(request, article_id, slug):
    if request.method == 'POST':
        id = request.POST.get('article_id')
        data = {}
        try:
            # Articles.objects.filter(id=article_id).delete()
            article = Articles.objects.get(id=article_id)
            article.status = 'DEL'
            article.save()
            data['result'] = "success"
            return HttpResponse(json.dumps(data), content_type='application/json')
        except:
            data['result'] = "fail"
            return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def editor_userbrief(request):
    if request.method == 'POST':
        name = request.session.get('user_name')
        user = get_object_or_404(BlogUser, name=name)
        data = {}
        try:
            user.brief = request.POST.get('briefcontent')
            user.save()
            data['result'] = get_object_or_404(BlogUser, name=name).brief
            data['flag'] = 'success'
            return HttpResponse(json.dumps(data), content_type='application/json')
        except:
            data['result'] = get_object_or_404(BlogUser, name=name).brief
            data['flag'] = 'fail'
            return HttpResponse(json.dumps(data), content_type='application/json')


def collect_cpu():
    t = time.strftime('%Y:%M:%S', time.localtime())  # 获取系统时间（只取分:秒）
    cpu = psutil.cpu_percent(interval=1, percpu=True)[0]  # 获取系统cpu使用率 non-blocking
    cpu = round(cpu / 100, 2)
    mem = psutil.virtual_memory()[2]
    mem = round(mem / 100, 2)
    disk_usage = psutil.disk_usage('/')[3]
    disk_usage = round(disk_usage / 100, 2)
    models.Sysrecord.objects.create(cpu=cpu, mem=mem, disk_usage=disk_usage)
    print(t, cpu)


def pyeditor(request):
    return render(request, 'blog/pyexplain.html')


def run_code(code):
    try:
        output = subprocess.check_output(['python', '-c', code],
                                         universal_newlines=True,
                                         stderr=subprocess.STDOUT,
                                         timeout=30)
        print(output)
    except subprocess.CalledProcessError as e:
        output = e.output
    except subprocess.TimeoutExpired as e:
        output = '\r\n'.join(['Time Out!!!', e.output])
    return output


@csrf_exempt
@require_POST
def api(request):
    code = request.POST.get('code')
    output = run_code(code)
    return JsonResponse(data={'output': output})


@csrf_exempt
def upload_images(request, article_id):
    pic = request.FILES['editormd-image-file']
    # article = Articles.objects.get(id=article_id)
    data = {}
    try:
        obj = models.ArticleBodyPic(article_id=article_id, pic=pic)
        obj.save()
        data = {
            "success": 1,
            "message": 'success',
            "url": obj.pic.url,
        }
    except:
        data = {
            "success": 0,
            "message": 'fail',
        }

    return HttpResponse(json.dumps(data), content_type='application/json')


def recruitment(request):
    recruitment = Recruitment.objects.all()
    recruitmentinfo = Recruinfo.objects.all()
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    tags = Tag.objects.all()
    categorys = Category.objects.all()
    context = {
        'recruitment': recruitment,
        'recruitmentinfo': recruitmentinfo,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'categorys': categorys,

    }
    return render(request, 'blog/recruitment.html', context=context)


def recruitmentinfo(request):
    recruitmentinfo = Recruinfo.objects.all()
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    tags = Tag.objects.all()
    categorys = Category.objects.all()
    context = {
        'recruitmentinfo': recruitmentinfo,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'categorys': categorys,
    }
    return render(request, 'blog/recruitmentinfo.html', context=context)


def findme(request):
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    tags = Tag.objects.all()
    categorys = Category.objects.all()
    context = {
        'recruitmentinfo': recruitmentinfo,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'categorys': categorys,
    }
    return render(request, 'blog/findme.html', context=context)


def movie_list(request):
    '''next = request.GET.get("next", '')
        print(f"next = {next}")
        path = "/".join(request.path.split("/")[3:])
        print(f"request.path= {request.path}")
        print(f"path = {path}")
        data = {"files":[], "dirs":[]}
        print(data)
        child_path = FILE_HOME_DIR+'/'+path
        print(f"child_path = {child_path}")
        data['cur_dir'] = path+next
        print(data)
        for dir in os.listdir(child_path):
        if os.path.isfile(child_path+"/"+dir):
        if os.path.splitext(dir)[1] in MEDIA:
        data['files'].append(dir)
        else:
        data['dirs'].append(dir)
        
        print(data)'''
    movielist = Movie.objects.all()
    context = {
        'films': movielist,
    }
    return render(request, "movielist.html", context)


def deletefile(request):
    data = {}
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        password = request.POST.get('password')
        right_password = models.params.objects.get(name='file_del_pwd').param_value
        if password == right_password:
            file_obj = models.JiaFile.objects.get(id=file_id)
            file_obj.file_status = '0'
            file_obj.save()
            data['result'] = 'success'
        else:
            data['result'] = 'fail'
        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def ajupload_file(request):
    data = {}
    if request.method == "POST":  # 请求方法为POST时，进行处理
        form = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        #        print(form,form.name)
        file_obj = models.JiaFile(file_name=form.name, file_url='static/Jia_File/' + form.name, file_status=1)
        file_obj.save()
        destination = open(os.path.join("static/Jia_File", form.name), 'wb')  # 打开特定的文件进行二进制的写操作
        for chunk in form.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        data['result'] = 'success'
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        data['result'] = 'fail'
        form = UploadFileForm()
        return HttpResponse(json.dumps(data), content_type='application/json')


def filecheck(request):
    data = {}
    if request.method == 'POST':
        password = request.POST.get('password')
        right_password = models.params.objects.get(name='file_down_pwd').param_value
        if password == right_password:
            data['result'] = 'success'
        else:
            data['result'] = 'fail'
        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def collect(request):
    if request.method == "POST":
        if request.session.get('is_login') == None:
            data = {}
            data["result"] = "illegal"
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {}
            blog_id = request.POST.get('article_id')
            name = request.session.get('user_name')
            name_id = str(BlogUser.objects.get(name=name).id)
            # thisarticle = get_object_or_404(Articles, id=blog_id)
            # thisarticle.increase_views()
            if BlogUserCollect.objects.filter(blogid=blog_id).count() >= 1:
                data["result"] = "fail"
            else:
                obj = BlogUserCollect(blogid=blog_id, userid=name_id)
                obj.save()
                data["result"] = "success"
            return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def editor_addcategory(request):
    if request.method == 'POST':
        name = request.session.get('user_name')
        user = get_object_or_404(BlogUser, name=name)
        data = {}
        try:
            newcategory = request.POST.get('newcategory')
            obj = Category(name=newcategory)
            obj.save()
            data['result'] = get_object_or_404(Category, name=newcategory).name
            data['flag'] = 'success'
            return HttpResponse(json.dumps(data), content_type='application/json')
        except:
            # data['result'] = get_object_or_404(Category, name=newcategory).name
            data['flag'] = 'fail'
            return HttpResponse(json.dumps(data), content_type='application/json')


def china_wuhan(request):
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver

    try:
        target = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579579384&enterid=1579579384&from=groupmessage&isappinstalled=0'
        # req = requests.get(url=target)
        # req.encoding = 'urf-8'
        # html = req.text
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 设置option,后台运行
        driver = webdriver.Chrome(chrome_options=option)
        driver.get(target)
        js = "var q=document.documentElement.scrollTop=1500"
        driver.execute_script(js)
        selenium_page = driver.page_source
        driver.quit()
        soup = BeautifulSoup(selenium_page, 'html.parser')
        cities = soup.find('div', {'class': 'areaBox___3jZkr'})
        # 每个省
        protocols = cities.find_all('div')
        data = {}

        for i in protocols:
            try:
                first = i.find('div', {'class': 'areaBlock1___3V3UU'})
                content = first.find_all('p')
                name = content[0].get_text()
                num = content[1].get_text()
                if num == "":
                    num = 0
                data['{}'.format(name)] = num
            except AttributeError as e:
                continue
    except:
        data = {}

    protocols = ["南海诸岛", '北京', '天津', '上海', '重庆', '河南',
                 '云南', '辽宁', '黑龙江', '湖南', '安徽', '山东',
                 '新疆', '江苏', '浙江', '江西', '湖北', '广西',
                 '甘肃', '山西', '内蒙古', '吉林', '福建', '贵州',
                 '广东', '青海', '西藏', '四川', '宁夏', '海南',
                 '台湾', '香港', '澳门'
                 ]

    context = {
        # 'protocols': protocols,
        'data': data
    }
    return render(request, 'china-wuhan.html', context=context)


def china_wuhan_virus(request):
    if request.method == 'GET':
        import requests
        from bs4 import BeautifulSoup
        from selenium import webdriver

        target = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579579384&enterid=1579579384&from=groupmessage&isappinstalled=0'
        req = requests.get(url=target)
        req.encoding = 'urf-8'
        html = req.text
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 设置option,后台运行
        driver = webdriver.Chrome(chrome_options=option)
        driver.get(target)
        js = "var q=document.documentElement.scrollTop=1500"
        driver.execute_script(js)
        selenium_page = driver.page_source
        driver.quit()
        soup = BeautifulSoup(selenium_page, 'html.parser')
        cities = soup.find('div', {'class': 'areaBox___3jZkr'})
        # 每个省
        protocols = cities.find_all('div')
        # data = []
        data = {}
        for i in protocols:
            try:
                # protocol = {}
                first = i.find('div', {'class': 'areaBlock1___3V3UU'})
                content = first.find_all('p')
                name = content[0].get_text()
                num = content[1].get_text()
                if num == "":
                    num = 0
                data['{}'.format(name)] = num
                # data.append(protocol)
            except AttributeError as e:
                continue

        # return HttpResponse(json.dumps(data), content_type='application/json')
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


class RssFeed(Feed):
    # 标题
    title = 'arithmeticjia的个人博客'
    # 描述
    description = 'https://www.guanacossj.com'
    # 链接
    link = "/"

    def items(self):
        # 返回所有文章
        return Articles.objects.all()

    def item_title(self, item):
        # 返回文章标题
        return item.title

    def item_description(self, item):
        # 返回文章内容
        return item.body[:30]

    def item_link(self, item):
        # 返回文章详情页的路由
        return reverse('blog:article', args=(item.id, item.url_slug))


def search_file(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/searchfile.html', {'error_msg': error_msg})

    file_list = JiaFile.objects.filter(file_name__icontains=q)
    oauth2_from = ''
    if request.user.username:
        name = request.user.username
        d_user_id = User.objects.get(username=name).id
        try:
            oauth2login = SocialAuthUsersocialauth.objects.get(user_id=d_user_id)
            oauth2_from = oauth2login.provider
        except Exception as e:
            # oauth2_name = ' '
            oauth2_from = 'Django'
    file_name = []
    for filename in os.listdir(r'static/Jia_File'):
        file_name.append(filename)
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    tags = Tag.objects.all()
    categorys = Category.objects.all()
    jia = Jia.objects.get(id=1)
    try:
        version = models.Version.objects.filter(version_time=datetime.datetime.now().strftime('%Y-%m-%d')).values(
            'version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    except IndexError as err:
        version = models.Version.objects.order_by('-version_time')[0:1].values('version_content')
        versions = [item[key] for item in version for key in item][0].split(";")
    context = {
        'recruitmentinfo': recruitmentinfo,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'categorys': categorys,
        'file_name': file_name,
        'versions': versions,
        'jia': jia,
        'oauth2_from': oauth2_from,
        'file_list': file_list
    }
    return render(request, 'blog/searchfile.html', context=context)


@require_http_methods(["GET"])
def get_article_all(request):
    response = {}
    try:
        articles = Articles.objects.filter(status="有效").order_by("id")
        response['list'] = json.loads(
            core_serializers.serialize("json", articles, use_natural_foreign_keys=True, ensure_ascii=False))
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        for i in range(len(response['list'])):
            response['list'][i]['fields']['words_number'] = len(md.convert(response['list'][i]['fields']['body']))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@require_http_methods(["GET"])
def get_categroy_all(request):
    category_list = Category.objects.values('name').annotate(
        num_articles=Count('articles', filter=Q(articles__status='有效')))
    data = {}
    try:
        list = []
        for i in category_list:
            p_tmp = {
                "name": i['name'],
                "num_articles": i['num_articles']
            }
            list.append(p_tmp)
        data['list'] = list
        data['msg'] = 'success'
        data['error_num'] = 0
    except Exception as e:
        data['msg'] = str(e)
        data['error_num'] = 1
    return HttpResponse(json.dumps(data), content_type='application/json')


@require_http_methods(["GET"])
def get_article_category(request, blog_category):
    cate = get_object_or_404(Category, name=blog_category)
    response = {}
    try:
        articles = Articles.objects.filter(category=cate).filter(status="有效").order_by('id')
        response['list'] = json.loads(
            core_serializers.serialize("json", articles, use_natural_foreign_keys=True, ensure_ascii=False))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@require_http_methods(["GET"])
def get_article_tag(request, blog_tag):
    tag_name = get_object_or_404(Tag, name=blog_tag)
    response = {}
    try:
        tag = Tag.objects.filter(name=tag_name).first()
        articles = tag.articles_set.all().filter(status='有效')
        response['list'] = json.loads(
            core_serializers.serialize("json", articles, use_natural_foreign_keys=True, ensure_ascii=False))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@require_http_methods(["GET"])
def get_article_single(request, article_id):
    response = {}
    next_article_title = ""
    prev_article_title = ""
    next_article_id = 0
    prev_article_id = 0
    try:
        article_id = Articles.objects.get(status="有效", id=article_id).id
        article = Articles.objects.filter(status="有效").filter(id=article_id)
        try:
            prev_article_id = Articles.objects.filter(id__lt=article_id, status='有效').last().id
            prev_article_title = Articles.objects.get(id=prev_article_id).title
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1
        try:
            next_article_id = Articles.objects.filter(id__gt=article_id, status='有效').first().id
            next_article_title = Articles.objects.get(id=next_article_id).title
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1
        single_article = get_object_or_404(Articles, id=article_id, status="有效")
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        single_article.body = md.convert(single_article.body)
        n = single_article.body.count('<div class="codehilite">', 0, len(single_article.body))
        for i in range(n):
            single_article.body = re.sub(r'<span></span>',
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
                                         '<div class="codehilite" id="code{}">'.format(i, i), single_article.body, 1)
        single_article.body = single_article.body.replace("/media", "https://www.guanacossj.com/media")
        response['list'] = json.loads(
            core_serializers.serialize("json", article, use_natural_foreign_keys=True, ensure_ascii=False))
        response['error_num'] = 0
        response['msg'] = 'success'
        response['words_number'] = len(md.convert(single_article.body))
        response['markdown'] = single_article.body
        response['prev_article_title'] = prev_article_title
        response['next_article_title'] = next_article_title
        response['prev_article_id'] = prev_article_id
        response['next_article_id'] = next_article_id
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@require_http_methods(["GET"])
def single_article(request, rand_id):
    response = {}
    next_article_title = ""
    prev_article_title = ""
    next_article_id = 0
    prev_article_id = 0
    prev_article_rand_id = ''
    next_article_rand_id = ''
    try:
        article_id = Articles.objects.get(status="有效", rand_id=rand_id).id
        article = Articles.objects.filter(status="有效").filter(rand_id=rand_id)
        try:
            prev_article_id = Articles.objects.filter(id__lt=article_id, status='有效').last().id
            prev_article_title = Articles.objects.get(id=prev_article_id).title
            prev_article_rand_id = Articles.objects.get(id=prev_article_id).rand_id
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1
        try:
            next_article_id = Articles.objects.filter(id__gt=article_id, status='有效').first().id
            next_article_title = Articles.objects.get(id=next_article_id).title
            next_article_rand_id = Articles.objects.get(id=next_article_id).rand_id
        except Exception as e:
            response['msg'] = str(e)
            response['error_num'] = 1
        single_article = get_object_or_404(Articles, id=article_id, status="有效")
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        single_article.body = md.convert(single_article.body)
        n = single_article.body.count('<div class="codehilite">', 0, len(single_article.body))
        for i in range(n):
            single_article.body = re.sub(r'<span></span>',
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
                                         '<div class="codehilite" id="code{}">'.format(i, i), single_article.body, 1)
        single_article.body = single_article.body.replace("/media", "https://www.guanacossj.com/media")
        response['list'] = json.loads(
            core_serializers.serialize("json", article, use_natural_foreign_keys=True, ensure_ascii=False))
        response['error_num'] = 0
        response['msg'] = 'success'
        response['markdown'] = single_article.body
        response['words_number'] = len(md.convert(single_article.body))
        response['prev_article_title'] = prev_article_title
        response['next_article_title'] = next_article_title
        response['prev_article_id'] = prev_article_id
        response['next_article_id'] = next_article_id
        response['prev_article_rand_id'] = prev_article_rand_id
        response['next_article_rand_id'] = next_article_rand_id
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return HttpResponse(json.dumps(response, ensure_ascii=False))


class JiaIndex(View):
    def get(self, request):
        blog_lists = Articles.objects.filter(status="有效").order_by("-timestamp")[0:9]  # 获取所有数据
        blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:5]  # 点击排行
        context = {
            'blog_list': blog_lists,
            'blog_list_views': blog_list_views
        }
        return render(request, 'newblog/index.html', context=context)


class JiaPostList(View):
    def get(self, request):
        try:
            blog_list = Articles.objects.filter(status="有效").order_by("-timestamp")  # 获取所有数据
            paginator = Paginator(blog_list, 15)  # 分页，每页15条数据
            page = request.GET.get('page')
            try:
                contacts = paginator.page(page)  # contacts为Page对象！
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                contacts = paginator.page(paginator.num_pages)
            context = {
                'contacts': contacts,
            }
            return render(request, 'newblog/archives.html', context=context)
        except:
            return render(request, '404.html')


class JiaPost(View):
    def get(self, request, article_id, slug):
        try:
            thisarticle = get_object_or_404(Articles, id=article_id, status='有效')
            if thisarticle.url_slug != slug:
                return render(request, '404.html')
            thisarticle.increase_views()
        except:
            return render(request, '404.html')
        thisarticle.increase_views()
        greats = thisarticle.greats
        category_id = thisarticle.category.id
        category = get_object_or_404(Category, id=category_id)
        thisarticle.body = markdown.markdown(thisarticle.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            # TocExtension(slugify=slugify)
        ])
        n = thisarticle.body.count('<div class="codehilite">', 0, len(thisarticle.body))
        m = thisarticle.body.count('<code>', 0, len(thisarticle.body))
        for i in range(n):
            thisarticle.body = re.sub(r'<span></span>',
                                      '&nbsp;&nbsp;<button id="ecodecopy" '
                                      'style="float: right;z-index:10" '
                                      'class="copybtn" '
                                      'data-clipboard-action="copy" '
                                      'data-clipboard-target="#code{}">复制</button> '
                                      '<div class="codehilite" id="code{}">'.format(i, i), thisarticle.body, 1)
        for i in range(m):
            thisarticle.body = re.sub(r'<code>',
                                      '<code style="background: rgba(205,205,205,0.51)">', thisarticle.body, 1)
        comment_list = thisarticle.comment_set.all()
        # thisarticle.body = md.convert(thisarticle.body)
        tag_name = thisarticle.tags.values('name')
        tag_name = [item[key] for item in tag_name for key in item]
        tag = (" ".join(tag_name)).split(" ")
        context = {
            "greats": greats,
            'post': thisarticle,
            'category': category,
            'comment_list': comment_list,
            'tag': tag
        }
        return render(request, 'newblog/post.html', context=context)


class JiaSearch(View):
    def get(self, request):
        q = request.GET.get('q')
        error_msg = ''
        if not q:
            error_msg = '请输入关键词'
            return render(request, 'blog/archive.html', {'error_msg': error_msg})
        blog_list = Articles.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
        paginator = Paginator(blog_list, 15)  # 分页，每页15条数据
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        context = {
            'contacts': contacts,
        }
        return render(request, 'newblog/archives.html', context=context)


@csrf_exempt
def upload_facepic_springboot(request):
    data = {}
    try:
        form = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        # if not myFile:
        #     return HttpResponse("no files for upload!")
        file_obj = models.JiaFile(file_name=form.name, file_url='static/Jia_File/' + form.name, file_status=1)
        file_obj.save()
        destination = open(os.path.join("static/Jia_File", form.name), 'wb')  # 打开特定的文件进行二进制的写操作
        for chunk in form.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        data["code"] = 200
        data["message"] = "上传成功"
        data["data"] = file_obj.file_url
    except:
        form = UploadFileForm()
        data["code"] = 500
        data["message"] = "上传失败"
        data["data"] = ""

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required()
@csrf_exempt
def sign_in(request):
    return HttpResponse("ok", content_type='application/json')


class LoveFZYSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoveFZY
        fields = [
            'id',
            'type',
            'content'
        ]


class GetLoveFZYToDoList(ListAPIView):
    serializer_class = LoveFZYSerializer
    queryset = LoveFZY.objects.filter(type=1).order_by('id')
    permission_classes = [AllowAny]


class GetLoveFZYDownList(ListAPIView):
    serializer_class = LoveFZYSerializer
    queryset = LoveFZY.objects.filter(type=0).order_by('id')
    permission_classes = [AllowAny]


class GetLoveFZYTimeline(ListAPIView):
    serializer_class = LoveFZYSerializer
    queryset = LoveFZY.objects.filter(type=2).order_by('id')
    permission_classes = [AllowAny]


class PostLoveFZYInfo(APIView):

    def post(self, request):
        data = request.data
        serializer = LoveFZYSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


def show_tags(request):
    response = {}
    tag_list = Tag.objects.annotate(num_posts=Count('articles')).filter(num_posts__gt=0)
    response["data"] = json.loads(
        core_serializers.serialize("json", tag_list, ensure_ascii=False))
    return HttpResponse(json.dumps(response, ensure_ascii=False))


@csrf_exempt
def upload_resumes(request):
    data = {}
    if request.method == "POST":
        form = request.FILES.get("file", None)
        file_obj = models.JiaFile(file_name=form.name, file_url='media/resume/' + form.name, file_status=1)
        file_obj.save()
        destination = open(os.path.join("media/resume", form.name), 'wb')  # 打开特定的文件进行二进制的写操作
        for chunk in form.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        data['result'] = 'success'
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        data['result'] = 'fail'
        return HttpResponse(json.dumps(data), content_type='application/json')


def love_fzy(request):
    return render_to_response("lovepic.html")
