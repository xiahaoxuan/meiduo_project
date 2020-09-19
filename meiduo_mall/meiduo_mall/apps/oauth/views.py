# 系统
import re
import logging

# Django
from django import http
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login
from django_redis import get_redis_connection
from django.shortcuts import render, redirect
# 第三方
from QQLoginTool.QQtool import OAuthQQ

# 自定义
from users.models import User
from oauth.models import OAuthQQUser
from oauth.utils import generate_access_token, check_access_token
from meiduo_mall.utils.response_code import RETCODE
from carts.utils import merge_cart_cookie_to_redis

# 创建日志输出器
logger = logging.getLogger('django')


class QQAuthURLView(View):
    """提供qq登录回调"""
    def get(self, request):
        next_url = request.GET.get('next')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI, state=next_url)
        login_url = oauth.get_qq_url()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'login_url': login_url})


class QQAuthUserView(View):
    """处理QQ登录回调"""
    def get(self, request):
        code = request.GET.get('code')
        if code is None:
            return http.HttpResponseForbidden('获取code失败')
        # 使用code获取access_token
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            access_token = oauth.get_access_token(code)
            # 使用access_token
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            return http.HttpResponseServerError('OAuth2.0认证失败')
            logger.error(e)
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            context = {'access_token_openid': generate_access_token(openid)}
            return render(request, 'oauth_callback.html', context)
        else:
            login(request, oauth_user.user)
            response = redirect(reverse('contents:index'))
            response.set_cookie('username', oauth_user.user.username, max_age=3600*24*15)
            response = merge_cart_cookie_to_redis(request=request, user=user, response=response)
            return response

    def post(self, request):
        """美多商城用户绑定到openid"""
        # 接收参数
        mobile = request.POST.get('mobile')
        pwd = request.POST.get('password')
        sms_code_client = request.POST.get('sms_code')
        access_token_openid = request.POST.get('access_token_openid')

        # 校验参数
        # 判断参数是否齐全
        if not all([mobile, pwd, sms_code_client]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断短信验证码是否一致
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '无效的短信验证码'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '输入短信验证码有误'})
        # 判断openid是否有效
        openid = check_access_token(access_token_openid)
        if not openid:
            return render(request, 'oauth_callback.html', {'openid_errmsg': 'openid已失效'})
            # 保存注册数据
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 用户不存在,新建用户
            user = User.objects.create_user(username=mobile, password=pwd, mobile=mobile)
        else:
            # 如果用户存在，检查用户密码
            if not user.check_password(pwd):
                return render(request, 'oauth_callback.html', {'account_errmsg': '用户名或密码错误'})
        # 将用户绑定openid
        try:
            OAuthQQUser.objects.create(openid=openid, user=user)
        except Exception as e:
            logger.error(e)
            return render(request, 'oauth_callback.html', {'qq_login_errmsg': 'QQ登录失败'})

        # 实现状态保持
        login(request, user)

        # 响应绑定结果
        next_url = request.GET.get('state')
        response = redirect(next_url)
        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        response = merge_cart_cookie_to_redis(request=request, user=user, response=response)
        return response



