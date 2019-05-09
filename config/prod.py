# -*- coding: utf-8 -*-
from config import RUN_VER
if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 正式环境
RUN_MODE = 'PRODUCT'

# 正式环境的日志级别可以在这里配置
# V2
# import logging
# logging.getLogger('root').setLevel('INFO')


# 正式环境数据库可以在这里配置
DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': APP_CODE,
            'USER': 'root',
            'PASSWORD': 'Uqv.83WuNm',
            'HOST': '10.0.1.192',
            'PORT': '3306',
        },
    }
)
