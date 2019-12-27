from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from django.db import connection


def login(request):
    if request.session.get('is_login', None):
        message = '您已登录'
        return render(request, 'login/login.html', locals())
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "请检查填写的内容"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                request.session['is_login'] = True
                request.session['username'] = username
                request.session['id'] = user.id
                return redirect("/scoringsystem/")
            else:
                message = "用户名或密码错误!"
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = LoginForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_name = form.cleaned_data['name']
            password = form.cleaned_data['password2']

            if User.objects.filter(username__exact=username):
                message = '用户名已经存在'
                return render(request, 'login/register.html', locals())
            user = User.objects.create_user(username=username, password=password)
            user_profile = UserProfile(user=user, user_name=user_name)
            user_profile.save()
            return redirect("/accounts/login/")
    else:
        form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/scoringsystem")   # 主页面
    request.session.flush()
    return redirect("/scoringsystem/")


def update(request, pk, message=None):
    if request.session.get('id', None) == pk:
        user = get_object_or_404(User, pk=pk)
        user_profile = get_object_or_404(UserProfile, user=user)
        form = ProfileForm(initial={'username': user.username, 'password1': user.password, 'password2': user.password, 'name': user_profile.user_name})
        return render(request, 'login/update.html', {'form': form, 'message': message})


def profile_update(request, pk):
    if request.session.get('id', None) == pk:
        user = get_object_or_404(User, pk=pk)
        user_profile = get_object_or_404(UserProfile, user=user)

        if request.method == "POST":
            form = ProfileForm(request.POST)
            message = ""
            if form.is_valid():
                username = form.cleaned_data['username']
                try:
                    User.objects.get(username=username)
                    message = "用户名重复"
                    return update(request, pk, message)
                except ObjectDoesNotExist:
                    user.username = username
                    user_name = form.cleaned_data['name']
                    password = form.cleaned_data['password1']
                    user_profile.user_name = user_name
                    user.password = password
                    user.save()
                    user_profile.save()
                    message = "更新成功"
                    return update(request, pk, message)
    else:
        return redirect("/accounts/login")



