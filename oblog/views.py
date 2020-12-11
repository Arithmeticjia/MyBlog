from django.db import models
from django.conf import settings
from alipay import AliPay
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render
from oblog.models import Articles, Message, Tag, Category, Note, BlogUser
# from blog.models import Love
from .forms import CommentForm
from .models import Comment
import time
import os
import json
import requests
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from django.http.response import HttpResponse, HttpResponseBadRequest
from oblog import talk_machine
from wechatpy import WeChatClient
from django.core.mail import send_mail
from .forms import UserForm
from .forms import RegisterForm
from django.shortcuts import render
from . import models
import psutil
import datetime
import execjs
import urllib
import urllib.request
import urllib.parse
import markdown
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    return render_to_response('index.html')


def blog_index(request):
    # post = request.get_post(Articles, pk=pk)
    blog_list = Articles.objects.filter(status="有效").order_by("-timestamp")[0:10]  # 获取所有数据
    blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:10]  # 点击排行
    blog_list_greats = Articles.objects.filter(status="有效").order_by('-greats')[0:10]  # 猜你喜欢
    blog_list_comments = Articles.objects.filter(status="有效").order_by('-comments')[0:10]  # 博主推荐
    blog_list_comments_top = Articles.objects.filter(status="有效").order_by('-comments')[0:1]  # 博主推荐
    tags = Tag.objects.all()
    count = Articles.objects.filter(status="有效").count()
    maxarticle = Articles.objects.filter(status="有效").order_by('-views')[0:1]
    comment_list = Comment.objects.count()
    note = Note.objects.get(id=str(random.randint(1, Note.objects.count())))
    categorys = Category.objects.all()
    context = {
        'maxview': maxarticle,
        'blog_list': blog_list,
        'blog_list_views': blog_list_views,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'comment_list': comment_list,
        'tags': tags,
        'note': note,
        'count': count,
        'categorys': categorys,
        'blog_list_comments_top': blog_list_comments_top,
    }
    return render(request, 'oblog/index.html', context=context)  # 返回index.html页面


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'oblog/list.html', {'error_msg': error_msg})

    blog_list = Articles.objects.filter(title__icontains=q)
    paginator = Paginator(blog_list, 15)  # 分页，每页10条数据
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
    comments = Comment.objects.count()
    tags = Tag.objects.all()
    view = []
    count = Articles.objects.count()
    pagelist = round(count / 5)
    pl = []
    for i in range(pagelist):
        pl.append(i + 1)
    # print((pl))
    # maxid = Articles.objects.all().aggregate(Max('views'))
    # maxid = maxid['id__max']
    for ids in range(1, count + 1):
        article = get_object_or_404(Articles, id=str(ids))
        print(article)
        view.append(article.increase_views())
    maxview = int(view.index(max(view))) + 1
    # maxarticle = Articles.objects.filter(views=maxid['views__max']+1)
    maxarticle = Articles.objects.filter(id=maxview)
    categorys = Category.objects.all()
    context = {
        'maxview': maxarticle,
        'blog_list': blog_list,
        'blog_list_views': blog_list_views,
        'tags': tags,
        'pagelists': pl,
        'contacts': contacts,
        'blog_list_greats': blog_list_greats,
        'comments': comments,
        'error_msg': error_msg,
        'categorys': categorys,
    }
    return render(request, 'oblog/list.html', context=context)


def blog_info(request, article_id):
    blogs = Articles.objects.count()  # 获取所有数据
    thisarticle = get_object_or_404(Articles, id=article_id)
    thisarticle.increase_views()
    greats = thisarticle.greats
    thisarticle.body = markdown.markdown(thisarticle.body,
                                         extensions=[
                                             'markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc',
                                         ])
    if int(article_id) == 1:
        leftarticle = '这已经是第一篇啦'
    else:
        leftarticle = get_object_or_404(Articles, id=str(int(article_id) - 1))
    if int(article_id) == int(Articles.objects.last().id):
        rightarticle = '这已经是最后一篇啦'
    else:
        rightarticle = get_object_or_404(Articles, id=str(int(article_id) + 1))
    comment_list = thisarticle.comment_set.all()
    maxarticle = Articles.objects.filter(status="有效").order_by('-views')[0:1]
    blog_list_all = Articles.objects.filter(status="有效").order_by("-views")[0:10]
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    blog_list_comments_top = Articles.objects.filter(status="有效").order_by('-comments')[0:1]  # 博主推荐
    category_id = thisarticle.category.id
    tag_name = thisarticle.tags.values('name')
    tag_name = [item[key] for item in tag_name for key in item]
    tag = (" ".join(tag_name))
    category = get_object_or_404(Category, id=category_id)
    comments = Comment.objects.count()
    note = Note.objects.get(id=str(random.randint(1, Note.objects.count())))
    categorys = Category.objects.all()
    context = {
        'blog_list_all': blog_list_all,
        'maxview': maxarticle,
        'blog_list': thisarticle,
        'comment_list': comment_list,
        'right_blog_list': rightarticle,
        'left_blog_list': leftarticle,
        'category': category,
        'tag': tag_name,
        'tags': tag,
        'greats': greats,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'comments': comments,
        'note': note,
        'categorys': categorys,
        'blog_list_comments_top': blog_list_comments_top,
    }
    return render(request, 'oblog/info.html', context=context)  # 返回info.html页面


def blog_list(request):
    # post = request.get_post(Articles, pk=pk)
    blog_list = Articles.objects.filter(status="有效").order_by("-timestamp")  # 获取所有数据
    blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:10]
    blog_list_greats = Articles.objects.filter(status="有效").order_by("-greats")[0:10]
    blog_list_comments = Articles.objects.filter(status="有效").order_by("-comments")[0:10]
    blog_list_comments_top = Articles.objects.filter(status="有效").order_by('-comments')[0:1]  # 博主推荐
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
    print(blog_list_views)
    tags = Tag.objects.all()
    view = []
    count = Articles.objects.count()
    pagelist = round(count / 3)
    pl = []
    for i in range(pagelist):
        pl.append(i + 1)
    maxarticle = Articles.objects.filter(status="有效").order_by('-views')[0:1]
    comments = Comment.objects.count()
    categorys = Category.objects.all()
    context = {
        'maxview': maxarticle,
        'blog_list': blog_list,
        'blog_list_views': blog_list_views,
        'tags': tags,
        'pagelists': pl,
        'contacts': contacts,
        'blog_list_greats': blog_list_greats,
        'blog_list_comments': blog_list_comments,
        'comments': comments,
        'categorys': categorys,
        'blog_list_comments_top': blog_list_comments_top,
    }
    # print((maxarticle))
    return render(request, 'oblog/list.html', context=context)


def aboutme(request):
    if request.method == 'GET':
        # 取出当前在models表中所有的留言信息 ,返回到前端
        allmessage = Message.objects.all()
        count = Articles.objects.count()
        blog_list_views = Articles.objects.filter(status="有效").order_by('-views')[0:10]  # 点击排行
        blog_list_greats = Articles.objects.filter(status="有效").order_by('-greats')[0:10]  # 猜你喜欢
        blog_list_comments = Articles.objects.filter(status="有效").order_by('-comments')[0:10]  # 博主推荐
        blog_list_comments_top = Articles.objects.filter(status="有效").order_by('-comments')[0:1]
        note = Note.objects.get(id=str(random.randint(1, Note.objects.count())))
        tags = Tag.objects.all()
        view = []
        maxarticle = Articles.objects.filter(status="有效").order_by('-views')[0:1]
        comment_list = Comment.objects.count()
        categorys = Category.objects.all()
        context = {
            'blog_list_views': blog_list_views,
            'maxview': maxarticle,
            'blog_list_greats': blog_list_greats,
            'blog_list_comments': blog_list_comments,
            "messages": allmessage,
            'tags': tags,
            'note': note,
            'comment_list': comment_list,
            'count': count,
            'categorys': categorys,
            'blog_list_comments_top': blog_list_comments_top,
        }
        return render(request, "oblog/about.html", context=context)
    return render_to_response('oblog/about.html')


# def getlove(request):
#     love = Love.objects.get(id=1)
#     now_time = datetime.date.today()
#     dif = (now_time-love.startdate).days
#     context = {
#         'love':love,
#         'now_time':now_time,
#         'dif':dif
#     }
#     return render(request,'love11.29.html',context=context)


def getlovepic(request):
    return render_to_response('lovepic.html')


def getnewweather(request):
    return render_to_response('myweather.html')


def getdocument(request):
    return render_to_response('oblog/document.html')


WECHAT_TOKEN = 'ssjsecrettoken980612ssj'
AppID = 'wx3200e87d6dd9eddd'
AppSecret = '3aade7b8bbf9cb305b076a1d2d0e4a71'

# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token='ssjsecrettoken980612ssj',
    appid='wx3200e87d6dd9eddd',
    appsecret='3aade7b8bbf9cb305b076a1d2d0e4a71'
)


def mymenu(request):
    # 第一个参数是公众号里面的appID，第二个参数是appsecret,个人微信公众号无法获得接口
    client = WeChatClient("wx3200e87d6dd9eddd", "3aade7b8bbf9cb305b076a1d2d0e4a71")
    client.menu.create({
        "button": [
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "视频",
                        "url": "http://v.qq.com/"
                    },

                ]
            }
        ],
    }
    )
    return HttpResponse('ok')


@csrf_exempt
def weixin(request):
    if request.method == "GET":
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        token = "ssjsecrettoken980612ssj"
        tmpArr = [token, timestamp, nonce]
        tmpArr.sort()
        string = ''.join(tmpArr).encode('utf-8')
        string = hashlib.sha1(string).hexdigest()
        if string == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("false")

    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()
    # 关注事件以及不匹配时的默认回复
    response = wechat_instance.response_text(
        content=(
            '感谢您的关注！\n本订阅号是智能机器人，回复任意内容开始聊天！谢谢您的关注\n'
            'Created By ArithmeticJia'

        ))

    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        if content == '你的真名叫什么':
            reply_text = '单沙嘉'
            response = wechat_instance.response_text(content=reply_text)

        elif content == '联系方式':
            reply_text = 'bluesaltssj@gmail.com'
            response = wechat_instance.response_text(content=reply_text)

        else:
            reply_text = talk_machine.talk(content)
            response = wechat_instance.response_text(content=reply_text)
    return HttpResponse(response, content_type="application/xml")


from django.http import FileResponse


def file_down(request):
    file = open('./static/download/0简易教学管理系统需求.doc', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="0简易教学管理系统需求.doc"'
    return response


# def getlocalweather(request):
#     url = "https://restapi.amap.com/v3/weather/weatherInfo"
#     key = '9bae4d790cfacdf4b54188b7758edf23'
#     data = {'key': key, "city": '320100'}
#     req = requests.post(url, data)
#     info = dict(req.json())
#     info = dict(info)
#     print(info)
#     newinfo = info['lives'][0]
#     print("你查询的当地天气信息如下：")
#     print("省市：", newinfo['province'] + newinfo['city'])
#     print("城市：", newinfo['city'])
#     print("编码：", newinfo['adcode'])
#     print("天气：", newinfo['weather'])
#     print("气温：", newinfo['temperature'] + '℃')
#     print("风向：", newinfo['winddirection'])
#     print("风力：", newinfo['windpower'])
#     print("湿度：", newinfo['humidity'])
#     print("报告时间：", newinfo['reporttime'])
#     newresult = newinfo['province'] + newinfo['city'] + ' 天气:' + newinfo['weather'] + ' 气温:' + newinfo[
#         'temperature'] + '℃' + ' 风向:' + newinfo['winddirection'] \
#                 + ' 风力:' + newinfo['windpower'] + ' 风向:' + newinfo['winddirection'] + ' 湿度:' + newinfo['humidity']
#
#     result = {
#         'location': newinfo['province'] + newinfo['city'],
#         'weather': newinfo['weather'],
#         'temperature': newinfo['temperature'] + '℃',
#         'winddirection': newinfo['winddirection'],
#         'windpower': newinfo['windpower'],
#         'humidity': newinfo['humidity'],
#         'reporttime': newinfo['reporttime'],
#     }
#     return render(request, 'myweather.html', result)


def sendemail(request):
    email_title = '邮件标题'
    email_body = '邮件内容'
    email = '1524126437@qq.com'  # 对方的邮箱
    send_mail(email_title, email_body, '1524126437@qq.com', [email])
    return render_to_response('myweather.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/Blog/monitor/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/Blog/monitor/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/Blog/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/oblog/new/")
    # request.session.flush()
    # 或者使用下面的方法
    del request.session['is_login']
    del request.session['user_id']
    del request.session['user_name']
    return redirect("/oblog/monitor/")


def newindex(request):
    # request.session.flush()
    return render(request, 'loginindex.html')


def getCPUInfo(request):
    a = psutil.cpu_times_percent()
    user_percentage = a.user
    system_percentage = a.system
    print("user and system are ", user_percentage, system_percentage)
    return HttpResponse('{"user": %s,"system":%s}' % (user_percentage, system_percentage))


def getMemInfo(request):
    m = psutil.virtual_memory()
    total_mem = m.total / 1024 / 1024
    used_mem_percentage = m.percent
    free_mem_percentage = 100 - m.percent
    print('{"total_mem":%s,"used_mem": %s,"free_mem":%s}' % (total_mem, used_mem_percentage, free_mem_percentage))
    return HttpResponse(
        '{"total_mem":%s,"used_mem": %s,"free_mem":%s}' % (total_mem, used_mem_percentage, free_mem_percentage))


def getDiskioData(request):
    diskioinfo = psutil.disk_io_counters(perdisk=True)
    disk_list = []
    for d in diskioinfo.keys():
        disk_list.append(d)
    return HttpResponse('{"disk_list":%s}' % (disk_list))


def monitor(request):
    return render(request, 'monitorindex.html')


def savemessage(request):
    username = request.POST.get("username")
    title = request.POST.get("title")
    content = request.POST.get("content")
    email = request.POST.get("email")
    publish = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email_title = '每一点进步离不开你的宝贵意见，由衷感谢你的支持~'
    email_body = '已经收到你的宝贵意见，我们会持续改进。--From ArithmeticJia'
    email = email  # 对方的邮箱
    send_mail(email_title, email_body, '1524126437@qq.com', [email])
    message = models.Message(title=title, content=content, username=username, email=email, publish=publish)
    message.save()

    return HttpResponseRedirect('/Blog/about/')


def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data


def inputtranslate(request):
    return render(request, 'translate.html')


def translate(request):
    if request.method == "POST":
        content = request.POST.get('content', None)
        js = eval('Py4Js()')
        tk = js.getTk(content)
        content = urllib.parse.quote(content)
        url = "http://translate.google.cn/translate_a/single?client=t" + "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" + "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" + "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (
        tk, content)
        result = open_url(url)
        end = result.find("\",")
        if end > 4:
            end = result[4:end]
            return render_to_response("oblog/show.html", {"translates": end})
        return render(request, 'oblog/show.html')


class Py4Js():

    def __init__(self):
        self.ctx = execjs.compile("""
            function TL(a) {
            var k = "";
            var b = 406644;
            var b1 = 3293161072;
            
            var jd = ".";
            var $b = "+-a^+6";
            var Zb = "+-3^+b+-f";
            
            for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
            }
            a = b;
            for (f = 0; f < e.length; f++) a += e[f],
            a = RL(a, $b);
            a = RL(a, Zb);
            a ^= b1 || 0;
            0 > a && (a = (a & 2147483647) + 2147483648);
            a %= 1E6;
            return a.toString() + jd + (a ^ b)
            };
            
            function RL(a, b) {
            var t = "a";
            var Yb = "+";
            for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
            }
            return a
            }
            """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


def videotest(request):
    return render_to_response('videotest.html')


def videoplayer(request, film_name):
    videoid = {
        'video_id': film_name,
    }
    return render(request, 'videoplayer.html', context=videoid)


FILE_HOME_DIR = "./static/film"
MEDIA = [".mp4", ]


def movie_list(request):
    next = request.GET.get("next", '')
    print(f"next = {next}")
    path = "/".join(request.path.split("/")[3:])
    print(f"request.path= {request.path}")
    print(f"path = {path}")
    data = {"files": [], "dirs": []}
    print(data)
    child_path = FILE_HOME_DIR + '/' + path
    print(f"child_path = {child_path}")
    data['cur_dir'] = path + next
    print(data)
    for dir in os.listdir(child_path):
        if os.path.isfile(child_path + "/" + dir):
            if os.path.splitext(dir)[1] in MEDIA:
                data['files'].append(dir)
        else:
            data['dirs'].append(dir)

    print(data)
    return render(request, "video.html", data)


@csrf_exempt
def comment_view(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = article
            comment.save()
            Articles.objects.update(comments=article.all_comments.count())
            return redirect('/oblog/article/%s' % (article_id))
        else:
            pass

    return HttpResponse("")


def timeline(request):
    return render_to_response('oblog/newtimeline.html')


def greats(request, article_id):
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
    # return render(request, 'info.html', context=context)  # 返回info.html页面
    return redirect('/oblog/article/%s' % (article_id))


def blog_category(request, blog_category):
    blog_list = Articles.objects.filter(category__name__exact=blog_category)  # 获取所有数据
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
    view = []
    count = Articles.objects.count()
    pagelist = round(count / 5)
    pl = []
    for i in range(pagelist):
        pl.append(i + 1)
    for ids in range(1, count + 1):
        article = get_object_or_404(Articles, id=str(ids))
        print(article)
        view.append(article.increase_views())
    maxview = int(view.index(max(view))) + 1
    # maxarticle = Articles.objects.filter(views=maxid['views__max']+1)
    maxarticle = Articles.objects.filter(id=maxview)
    categorys = Category.objects.all()
    context = {
        'maxview': maxarticle,
        'blog_list': blog_list,
        'blog_list_views': blog_list_views,
        'blog_list_comments': blog_list_comments,
        'tags': tags,
        'pagelists': pl,
        'contacts': contacts,
        'blog_list_greats': blog_list_greats,
        'comments': comments,
        'categorys': categorys,
        'blog_category': blog_category,
    }
    return render(request, 'list.html', context=context)


def login(request):
    if request.session.get('is_login', None):
        return redirect('/oblog/monitor/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.BlogUser.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    print(request.session['is_login'], request.session['user_name'])
                    return redirect('/oblog/monitor/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'oblog/login.html', locals())

    login_form = UserForm()
    return render(request, 'oblog/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/oblog/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'oblog/register.html', locals())
            else:
                same_name_user = models.BlogUser.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'oblog/register.html', locals())
                same_email_user = models.BlogUser.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'oblog/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.BlogUser.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/oblog/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'oblog/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/oblog/newindex/")
    # request.session.flush()
    # 或者使用下面的方法
    del request.session['is_login']
    del request.session['user_id']
    del request.session['user_name']
    return redirect("/oblog/login/")
