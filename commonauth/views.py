from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponse, render, redirect


# Create your views here.
from blogproject import models
from blogproject.models import User


def do_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next_url")

        try:
            user = authenticate(username=username, password=password)
            if user.is_active:
                    login(request, user)
                    if next_url and next_url != "/auth/logout/":
                        response = redirect(next_url)
                    else:
                        response = redirect("/blog/index/")
                    return response
            else:
                message = "用户状态信息异常，请联系管理员(18351922995)! "

        except:
            message = "用户不存在！"
        return render(request, 'blogproject/login.html', locals())
    else:
        next_url = request.GET.get("next", '')
        return render(request, "blogproject/login.html", {'next_url': next_url}, locals())


def do_logout(request):

    logout(request)

    return redirect("/blog/login/")