# 定义任务
from celery_task.sms.SendMessage import send_message
from meiduo_mall.utils import constants
from celery_task.main import celery_app


@celery_app.task(bind=True, name='send_sms_code', retry_backoff=3)
def send_sms_code(self, mobile, sms_code):
    try:
        send_ret = send_message(constants.SEND_SMS_TEMPLATE_ID, mobile,
                                (sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60))
    except Exception as e:
        raise self.retry(exec=e, max_retries=3)
    return send_ret
