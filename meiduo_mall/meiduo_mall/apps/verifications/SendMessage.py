from ronglian_sms_sdk import SmsSDK
import json

accId = '8aaf0708732220a601746204d165071b'
accToken = 'ec0a49c230ff4b2b8b8f15c2494fc00a'
appId = '8aaf0708732220a601746207e2e8072e'


def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    sdk.sendMessage(1, '13348685262', ('12345', 2))


class CCP(object):
    def __new__(cls, *args, **kwargs):
        """
        :return 单例
        """
        if not hasattr(cls, '_instance'):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # 初始化SDK
            cls._instance.sdk = SmsSDK(accId, accToken, appId)
            return cls._instance

    def send_template_sms(self, tid, mobile, datas):
        result = self._instance.sdk.sendMessage(tid, mobile, datas)
        json_dic = json.loads(result)
        if json_dic.get('statusCode') == '000000':
            return 0
        else:
            return -1


if __name__ == '__main__':
    CCP().send_template_sms(1, '13348685262', ('12345', 2))
