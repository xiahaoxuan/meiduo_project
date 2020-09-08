# 定义任务
from celery_task.sms.SendMessage import send_message
from meiduo_mall.utils import constants
from celery_task.main import celery_app


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    send_ret = send_message(constants.SEND_SMS_TEMPLATE_ID, mobile, (sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60))
    return send_ret
