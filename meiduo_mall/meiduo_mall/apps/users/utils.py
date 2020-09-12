# 自定义用户认证的后端
import re

from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData

from users.models import User
from . import constants


def generate_verify_email_url(user):
    """生成邮箱激活链接"""
    s = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {'user_id': user.id, 'email': user.email}
    token = s.dumps(data)
    #
    email_url = settings.EMAIL_VERIFY_URL+'?token='+token.decode()
    return email_url


def check_verify_email_id(token):
    """发序列化生成id"""
    s = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data = s.loads(token)
    except BadData:
        return None
    user_id = data.get('user_id')
    email = data.get('email')
    try:
        user = User.objects.get(id=user_id, email=email)
    except User.DoesNotExist:
        return None

    return user







def get_user_by_account(account):
    """
    使用账号查询
    """
    try:
        if re.match(r'1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


def check_password(user, password):
    """
    校验密码
    """
    if user and user.check_password(password):
        return user
    else:
        return None


class UsernameMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 使用账号查询用户
        user = get_user_by_account(username)
        user = check_password(user, password)
        return user
