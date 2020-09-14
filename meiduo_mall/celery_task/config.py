# 指定中间人，消息队列，任务队列，容器，使用redis

from django.conf import settings

broker_url = "redis://" + settings.DEV_URL + ":6379/10"


