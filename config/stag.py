# -*- coding: utf-8 -*-
from config import RUN_VER
if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import  * # noqa

# 预发布环境
RUN_MODE = 'STAGING'

# 正式环境的日志级别可以在这里配置
# V2
# import logging
# logging.getLogger('root').setLevel('INFO')


# 预发布环境数据库可以在这里配置
# (以下内容修改为你自己的, 正式开发勿泄漏)

DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bay12',
            'USER': 'root',
            'PASSWORD': 'Uqv.83WuNm',
            'HOST': '10.0.1.192',
            'PORT': '3306',
        },
    }
)
