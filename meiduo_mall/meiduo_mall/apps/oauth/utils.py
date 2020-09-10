from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings
from . import constants


def generate_access_token(openid):
    """序列化"""
    s = Serializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    data = {'openid': openid}
    token = s.dumps(data)
    return token.decode()


def check_access_token(openid):
    """反序列化"""
    s = Serializer(settings.SECRET_KEY,constants.ACCESS_TOKEN_EXPIRES)
    try:
        data = s.loads(openid)
    except BadData:
        return None
    else:
        return data.get('openid')