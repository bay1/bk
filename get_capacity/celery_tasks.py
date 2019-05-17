# -*- coding: utf-8 -*-
import re
import time
import logging
import datetime
import base64

from celery import task
from celery.task import periodic_task

from config import APP_CODE
from get_capacity.models import DiskUsage, MemoryUsage
from blueapps.account.models import User
from blueking.component.shortcuts import get_client_by_user

logger = logging.getLogger('celery')


def base64_encode(string):
    """
    对字符串进行base64编码
    """
    return base64.b64encode(string).decode("utf-8")


def fast_execute_script(client, script_content, script_param):
    """
    快速执行脚本函数
    """
    kwargs = {
        "bk_app_code": APP_CODE,
        "bk_biz_id": 3,  # 业务ID 后台链接中可以查看
        # "script_id": 1,
        "script_content": script_content,
        "script_param": script_param,
        "script_timeout": 1000,
        "account": "root",
        "is_param_sensitive": 0,
        "script_type": 1,
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": "10.0.1.102"
            }
        ],
        "custom_query_id": [
            "3"
        ]
    }
    return client.job.fast_execute_script(kwargs)


def get_job_instance_log(client, job_instance_id):
    """
    对作业执行具体日志查询函数
    """

    kwargs = {
        "bk_app_code": APP_CODE,
        "bk_biz_id": 3,
        "job_instance_id": job_instance_id
    }
    time.sleep(2)  # todo 延时2s, 快速执行脚本需要一定的时间， 后期可以用celery串行两个函数
    return client.job.get_job_instance_log(kwargs)


def execute_script_log(script_content, script_param):
    """
    执行脚本命令，并获取执行log
    """
    user = User.objects.get(username='328588917')
    client = get_client_by_user(user.username)

    # base64 快速执行脚本需要的参数，并执行client
    fast_execute_script_result = fast_execute_script(client, script_content, script_param)

    # 如果快速脚本调用成功，执行log日志查询，获取执行内容
    if fast_execute_script_result['message'] == 'success':
        job_instance_id = fast_execute_script_result['data']['job_instance_id']
        get_job_instance_log_result = get_job_instance_log(client, job_instance_id)

        # 如果日志查询成功，提取内容
        if get_job_instance_log_result['message'] == 'success':
            # 匹配log_content规则
            regex = r"(?<='log_content': ').*?(?=')"

            return re.findall(regex, str(get_job_instance_log_result), re.MULTILINE)
    else:
        return None


@task()
def get_capacity_task():
    """
    定义一个获取磁盘使用率异步任务
    """
    script_content = base64_encode(b"df -h ${1} | awk '{if(+$5>0) print +$5}'")
    script_param = base64_encode(b'/')
    log_content = execute_script_log(script_content, script_param)

    if log_content is None:
        logger.info(u'request false')
    else:
        # 提取磁盘使用率->数字
        disk_usage = re.sub(r'\D', "", log_content[0])

        DiskUsage.objects.create(disk_usage=int(disk_usage))
        logger.info(u'disk usage = ' + disk_usage + '%, deposited into the database->success')


@task()
def get_capacity_memory():
    """
    定义一个获取内存使用率异步任务
    """
    script_content = base64_encode(b"free -m | sed -n '2p' | awk '{print(($3/$2)*100)}'")
    log_content = execute_script_log(script_content, script_param='')

    if log_content is None:
        logger.info(u'request false')
    else:
        # 提取磁盘使用率->数字
        memory_usage = int(re.sub(r'\D', "", log_content[0])) / 10000

        MemoryUsage.objects.create(memory_usage=memory_usage)
        logger.info(u'memory usage = ' + str(memory_usage) + '%, deposited into the database->success')


@periodic_task(run_every=datetime.timedelta(hours=1))
def get_capacity_periodic():
    """
    获取磁盘使用率周期执行定义
    """
    get_capacity_task.delay()
    get_capacity_memory.delay()
    logger.info(u'get capacity work starting')
