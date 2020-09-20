import os
from django.shortcuts import render
# Create your views here.
from django.views import View
from django import http
from django.conf import settings

from orders.models import OrderInfo
from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.views import LoginRequiredJsonMixin, LoginRequiredMixin

from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig


class PaymentView(LoginRequiredJsonMixin, View):
    def get(self, request, order_id):
        # 查询要支付的订单
        user = request.user
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单信息错误')
        app_private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem")
        alipay_public_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem")
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )
        # 生成登录支付宝连接
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject="美多商城%s" % order_id,
            return_url=settings.ALIPAY_RETURN_URL,
        )
        alipay_url = settings.ALIPAY_URL + "?" + order_string
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'alipay_url': alipay_url})
