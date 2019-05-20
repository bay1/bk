# -*- coding: utf-8 -*-
import json

from django.http import JsonResponse
from django.shortcuts import render

from config import APP_CODE
from home_application.models import Host
from blueking.component.shortcuts import get_client_by_request
from blueapps.account.decorators import login_exempt


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, 'home_application/home.html')


def hello(request):
    """
    测试页面
    """
    if request.method == 'POST':
        hello_form = json.loads(request.body)
        if hello_form and 'content' in hello_form.keys():
            result = {'message': 'Congratulation！' if hello_form['content'] == 'Hello Blueking' else 'None'}
            return JsonResponse(result)
    return render(request, 'home_application/hello.html')


def host_disk(request):
    """
    主机磁盘管理
    """

    hosts = Host.objects.all()
    return render(request, 'home_application/hostdisk.html', {'hosts': hosts})


def get_cchost_ips(request):
    """
    前端获取可以录入的主机IP的接口
    """
    client = get_client_by_request(request)
    kwags = {
        "bk_app_code": APP_CODE,
        "bk_biz_id": 3
    }
    cc_hosts = client.cc.search_host(kwags)['data']['info']
    cc_hosts_ips = []
    for host in cc_hosts:
        host = host['host']
        cc_hosts_ips.append({host['bk_host_innerip']: host['bk_os_name']})
    return JsonResponse({"data": cc_hosts_ips})


def get_host_ip(request):
    """
    前端获取主机IP的接口
    """
    hosts = Host.objects.all()
    check_ip = []
    host_ips = []
    for host in hosts:
        if host.ip not in check_ip:
            check_ip.append(host.ip)
            host_ips.append({"id": host.id, "text": host.ip, "system": host.system, "disk": host.disk})
    return JsonResponse({"results": host_ips})


def add_host(request):
    """
    录入主机记录
    """
    form_data = request.POST.dict()
    check_result = Host.check_form_data(**form_data)
    if check_result[0] and Host.objects.create(**form_data):
        return JsonResponse({"result": "success"})
    else:
        return JsonResponse({"result": "false", "message": check_result[1]})


def search_host(request):
    if request.method == 'POST':
        host_form = json.loads(request.body)
        if host_form and 'ip' in host_form.keys():
            hosts = Host.objects.filter(ip=host_form['ip']).values()
            return JsonResponse({'data': list(hosts)})


@login_exempt
def api_disk_usage(request):
    """
    磁盘使用率API接口
    """
    ip = request.GET.get('ip', '')
    system = request.GET.get('system', '')
    mounted = request.GET.get('disk', '')
    if ip and system and mounted:
        hosts = Host.objects.filter(ip=ip, system=system, disk=mounted)

    else:
        return JsonResponse({
            "result": False,
            "data": [],
            "message": '参数不完整'
        })

    data_list = []
    for _data in hosts:
        disk_usages = _data.DiskUsage.all()
        memory_usages = _data.MemoryUsage.all()
        disk_usage_add_time, disk_usage_value = model_data_format(disk_usages)
        memory_usage_add_time, memory_usage_value = model_data_format(memory_usages)

        data_list.append(
            {
                'ip': _data.ip,
                'system': _data.system,
                'mounted': _data.disk,
                'disk_usage': {
                    "xAxis": disk_usage_add_time,
                    "series": [
                        {
                            "name": "磁盘使用率",
                            "type": "line",
                            "data": disk_usage_value
                        }
                    ]
                },
                'memory_usage': {
                    "xAxis": memory_usage_add_time,
                    "series": [
                        {
                            "name": "内存使用率",
                            "type": "line",
                            "data": memory_usage_value
                        }
                    ]
                }
            }
        )

    return JsonResponse({
        "result": True,
        "data": data_list,
        "message": 'ok'
    })


def model_data_format(usages):
    usage_add_time = []
    usage_value = []
    for usage in usages:
        usage_add_time.append(usage.add_time.strftime("%Y/%m/%d %H:%M:%S"))
        usage_value.append(usage.value)
    return usage_add_time, usage_value
