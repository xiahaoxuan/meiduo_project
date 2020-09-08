from django.shortcuts import render
from django.views import View
from django import http
from django_redis import get_redis_connection
import random
import logging


from meiduo_mall.utils import constants
from meiduo_mall.utils.response_code import RETCODE
from verifications.libs.captcha.captcha import captcha
# from verifications.SendMessage import send_message
from celery_task.sms.tasks import send_sms_code

logger = logging.getLogger('django')


# Create your views here.
class SMSCodeView(View):
    def get(self, request, mobile):
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户是否频繁发送验证码
        redis_conn = get_redis_connection("verify_code")
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})

        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})
        redis_conn.delete('img_%s' % uuid)
        if image_code_client.lower() != image_code_server.decode().lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码有误'})
        sms_code = random_code()
        logger.info(sms_code)  # 手动输出日志，记录短信验证码
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()
        send_sms_code.delay(mobile, sms_code)

        # send_message(constants.SEND_SMS_TEMPLATE_ID, mobile, (sms_code, constants.SMS_CODE_REDIS_EXPIRES//60))
        # CCP().send_template_sms(constants.SEND_SMS_TEMPLATE_ID, mobile,
        #                         (sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60))

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送成功'})


def random_code():
    """生成6位随机码"""
    code_list = []
    sms_code = ''
    for i in range(10):
        code_list.append(str(i))
    code_list = random.sample(code_list, 6)
    for s in code_list:
        sms_code += s
    return sms_code


class ImageCodeView(View):
    def get(self, request, uuid):
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection("verify_code")
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        return http.HttpResponse(image, content_type='image/jpg')
        pass
