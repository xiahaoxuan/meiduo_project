from django.shortcuts import render
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
# Create your views here.
from django import http
from meiduo_mall.utils.response_code import RETCODE
import logging

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
            open_id = oauth.get_open_id(access_token)
        except Exception as e:
            return http.HttpResponseServerError('OAuth2.0认证失败')
            logger.error(e)
        state = request.GET.get('state')

