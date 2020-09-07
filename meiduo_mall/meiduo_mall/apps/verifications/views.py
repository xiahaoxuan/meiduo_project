from django.shortcuts import render
from django.views import View
from verifications.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django import http
from meiduo_mall.utils import constants
from meiduo_mall.utils.response_code import RETCODE
import random
from verifications.SendMessage import CCP


# Create your views here.
class SMSCodeView(View):
    def get(self, request, mobile):
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必传参数')
        redis_conn = get_redis_connection("verify_code")
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})
        redis_conn.delete('img_%s' % uuid)
        if image_code_client.lower() != image_code_server.decode().lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码有误'})
        code_list = []
        sms_code = ''
        for i in range(10):
            code_list.append(str(i))
        code_list = random.sample(code_list, 6)
        for s in code_list:
            sms_code += s
        print(sms_code)
        ex = constants.SMS_CODE_REDIS_EXPIRES
        print(ex)
        redis_conn.setex('sms_%s' % mobile, ex, sms_code)
        CCP().send_template_sms(constants.SEND_SMS_TEMPLATE_ID, mobile, (sms_code, constants.SMS_CODE_REDIS_EXPIRES//60))
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送成功'})


class ImageCodeView(View):
    def get(self, request, uuid):
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection("verify_code")
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        return http.HttpResponse(image, content_type='image/jpg')
        pass

