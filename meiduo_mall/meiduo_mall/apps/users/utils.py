# 自定义用户认证的后端
import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


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
