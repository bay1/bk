# -*- coding: utf-8 -*-
import json
from django.http import JsonResponse
from django.shortcuts import render

from home_application.models import Host


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
            host_ips.append({"id": host.id, "text": host.ip})
    # {"results": [{"id": 0, "text": "奥迪"}, {"id": 1, "text": "奔驰"}, {"id": 1, "text": "宝马"}]
    return JsonResponse({"results": host_ips})


def add_host(request):
    """
    录入主机记录
    """
    form_data = request.POST.dict()
    if Host.objects.create(**form_data):
        return JsonResponse({"result": "success"})
    else:
        return JsonResponse({"result": "false"})


def search_host(request):
    if request.method == 'POST':
        host_form = json.loads(request.body)
        if host_form and 'ip' in host_form.keys():
            hosts = Host.objects.filter(ip=host_form['ip']).values()
            return JsonResponse({'data': list(hosts)})
