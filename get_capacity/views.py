# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
from django.http import JsonResponse

from home_application.models import Host
from blueking.component.shortcuts import get_client_by_request


def index(request):
    """
    定时获取使用率图表html展示
    """
    return render(request, 'get_capacity/index.html')


def get_usage_data(request):
    if request.method == 'POST':
        client = get_client_by_request(request)
        kwags = json.loads(request.body)
        test = client.self_server.get_dfusage_bay1(kwags)
        print(test)
        return JsonResponse(test)