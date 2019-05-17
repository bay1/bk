# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse

from get_capacity.models import DiskUsage, MemoryUsage
from blueapps.account.decorators import login_exempt


def index(request):
    """
    定时获取使用率图表html展示
    """
    return render(request, 'get_capacity/index.html')


@login_exempt
def get_disk_usages(request):
    """
    返回定时磁盘采集数据
    """
    disk_usages = DiskUsage.objects.all()
    disk_usage_add_time, disk_usage_value = model_data_format(disk_usages)

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


def get_memory_usages(request):
    """
    返回定时内存采集数据
    """
    memory_usages = MemoryUsage.objects.all()
    memory_usage_add_time, memory_usage_value = model_data_format(memory_usages)

    return JsonResponse({
        "result": True,
        "data": {
            "xAxis": memory_usage_add_time,
            "series": [
                {
                    "name": "内存使用率",
                    "type": "line",
                    "data": memory_usage_value
                }
            ]
        }})


def model_data_format(usages):
    usage_add_time = []
    usage_value = []
    for usage in usages:
        usage_add_time.append(usage.add_time.strftime("%Y/%m/%d %H:%M:%S"))
        usage_value.append(usage.value)
    return usage_add_time, usage_value
