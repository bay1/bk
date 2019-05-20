# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class Host(models.Model):
    ip = models.GenericIPAddressField(max_length=30)
    system = models.CharField(max_length=64)
    disk = models.CharField(max_length=30)
    add_time = models.DateTimeField('录入时间', auto_now=True)

    @staticmethod
    def check_form_data(**form_data):
        """
        对输入的数据进行检查
        :param form_data:
        :return:
        """
        # ip一致时，检查操作系统输入
        check_ip = Host.objects.filter(ip=form_data['ip']).values()
        if check_ip and form_data['system'] != check_ip[0]['system']:
            return False, 'ip系统已经存在'

        # ip一致时，检查是否已经输入此磁盘地址
        hosts_data = Host.objects.filter(ip=form_data['ip']).values()
        for host_data in list(hosts_data):
            if form_data['disk'] == host_data['disk']:
                return False, '此ip此磁盘已录入'
        return True, ''
