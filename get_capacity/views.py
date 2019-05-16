# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse

from get_capacity.models import DiskUsage


def index(request):
    """
    定时获取磁盘使用率图表html展示
    """
    return render(request, 'get_capacity/index.html')


def get_disk_usages(request):
    """
    返回定时磁盘采集数据
    """
    disk_usages = DiskUsage.objects.all()
    disk_usage_add_time = []
    disk_usage_value = []
    for disk_usage in disk_usages:
        disk_usage_add_time.append(disk_usage.add_time.strftime("%Y/%m/%d %H:%M:%S"))
        disk_usage_value.append(disk_usage.disk_usage)
    return JsonResponse({
        "result": True,
        "data": {
            "xAxis": disk_usage_add_time,
            "series": [
                {
                    "name": "磁盘使用率",
                    "type": "line",
                    "data": disk_usage_value
                }
            ]
        }})
