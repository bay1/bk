# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render


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
            return HttpResponse(json.dumps(result), content_type='application/json')
    return render(request, 'home_application/hello.html')
