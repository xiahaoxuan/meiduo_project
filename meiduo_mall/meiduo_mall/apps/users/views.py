import re

from django import http
from django.urls import reverse
from django.db import DatabaseError
from django_redis import get_redis_connection
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout

from users.models import User
from meiduo_mall.utils.response_code import RETCODE

# Create your views here.
from django.views import View


class UsernameCountView(View):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """提供用户注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        #  表单参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code_client = request.POST.get('sms_code')
        allow = request.POST.get('allow')

        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'register.html', {'sms_code_errmsg': '短信验证码失效'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'register.html', {'sms_code_errmsg': '短信验证码有误'})
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # return render(request, 'register.html', {'register_errmsg': '注册失败'})
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        login(request, user)
        # return redirect('/')
        return redirect(reverse('contents:index'))


class LoginView(View):
    """用户登录"""

    def get(self, request):
        """提供界面"""
        return render(request, 'login.html', {'login_errmsg': '登录失败'})
        pass

    def post(self, request):
        """实现用户登录逻辑"""
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        # 校验参数
        # 判断参数是否齐全
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')

        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码最少8位，最长20位')
        # 认证用户: 使用账户查询用户是否存在，如果用户存在，再校验密码是否正确
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '账号或密码错误'})
        # 状态保持
        login(request, user)
        # 使用remembered
        if remembered != 'on':
            # 没有记住登录
            request.session.set_expiry(0)
        else:
            # 记住登录状态保持周期为两周
            request.session.set_expiry(None)
        next_url = request.GET.get('next')
        if next_url:
            response = redirect(next_url)
        else:
            response = redirect(reverse('contents:index'))

        response.set_cookie('username', user.username, max_age=3600*24*15)
        # 响应结果
        return response


class LogoutView(View):

    def get(self, request):
        logout(request)
        response = redirect(reverse('contents:index'))
        # response.set_cookie('username', max_age=-1)
        response.delete_cookie('username')

        return response


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_info.html')






