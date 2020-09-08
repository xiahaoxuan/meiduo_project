# 安装启动celery
# python3 -m celery -A celery_task.main worker --loglevel INFO
# 报错需要安装 pip3 install --upgrade https://github.com/celery/celery/tarball/master

from celery import Celery

# 创建Celery实例
celery_app = Celery('meiduo')

# 加载配置
celery_app.config_from_object('celery_task.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_task.sms'])
