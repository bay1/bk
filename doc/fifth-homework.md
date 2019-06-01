Base: Windows + Python 3.6 + 蓝鲸框架2.0

### 向助手申请自主接入的，外网接口地址

>前面作业基础上，应该已经配好各种config

**自主接入在这次实验中的大概意思就是**：
- 自己写的API接口->'映射'到自主接入的外网接口地址
- 你的应用再从blueking/component/apis中接入这个外网接口地址，封装起来能供client直接调用

![api自主接入申请.png](https://smartpublic-10032816.file.myqcloud.com/custom/20190524130619/17266/20190524130619/--d7dc685a48175ee76821a63c7f71be46.png)

#### 书写自己写的API接口，不用登陆就能访问，添加装饰器@login_exempt

```python
@login_exempt
def api_disk_usage(request):
    """
    磁盘使用率API接口 api/get_dfusage_xxx
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
        disk_usage_add_time, disk_usage_value = model_data_format(disk_usages)

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

```
**这段代码在上篇文章中已经提到过，再次利用下
然后配置url, 注意这个要和你向助手沟通好的目标接口地址一致**

```python
url(r'^api/get_dfusage_xxx/$', views.api_disk_usage),
```

**然后部署应用，如果你直接访问，应用正式地址这个api接口地址回显成功，即success**

#### 封装到client

> 在blueking/component/apis添加你的接口文件，命名可以直接是get_dfusage_xxx

```python
# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsGetDfusagexxx(object):
    """Collections of get_dfusage_bay1 APIS"""

    def __init__(self, client):
        self.client = client

        self.get_dfusage_bay1 = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/self-service-api/api/get_dfusage_xxx/',
            description=u'获取指定磁盤容量'
        )
```
**其中的path即你和助手沟通好的注册API路径**

在blueking/component/collections.py 添加你刚才写的函数，比如

```python
from .apis.get_dfusage_xxx import CollectionsGetDfusagexxx

# Available components
AVAILABLE_COLLECTIONS = {
    ...
    'self_server': CollectionsGetDfusagexxx
}

```

#### 然后去你能添加url的view里定义调用自主接入的api

```python
# -*- coding: utf-8 -*-
import json

from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request

def get_usage_data(request):
    """
    调用自主接入接口api
    """
    if request.method == 'POST':
        client = get_client_by_request(request)
        kwargs = json.loads(request.body)
        usage = client.self_server.get_dfusage_xxx(kwargs)
        return JsonResponse(usage)
=====================================
url(r'^get_usage_data/$', views.get_usage_data) # url.py 配置 url
```

**注意这里的kwargs需要和你的定义参数相对应**

#### 前端展示和上次作业内容差不多，只是多三个参数的post
```html
<form class="form-horizontal>
    <div class="form-group clearfix">
        <label class="col-sm-3 control-label bk-lh30 pt0">IP地址：</label>
        <div class="col-sm-6">
            <select name="" id="host_ip" class="form-control bk-valign-top">
            </select>
        </div>
    </div>
    <div class="form-group clearfix">
        <label class="col-sm-3 control-label bk-lh30 pt0">系统：</label>
        <div class="col-sm-6">
            <input type="text" class="form-control bk-valign-top"></div>
    </div>
    <div class="form-group clearfix">
        <label class="col-sm-3 control-label bk-lh30 pt0">磁盘：</label>
        <div class="col-sm-6">
            <select name="" id="host_disk" class="form-control bk-valign-top">
            </select>
        </div>
    </div>
</form>
```

```js
    $("#submit-button").addEventListener('click', function () {
        var ip = $('#host_ip').val();
        var system = $('#host_system').val();
        var disk = $('#host_disk').val();
        console.log(ip, system, disk);
        let data = {
            'ip': ip,
            'system': system,
            'disk': disk
        };
        $.ajax({
            url: '{{ SITE_URL }}get_capacity/get_usage_data/',
            data: JSON.stringify(data),
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                if (data['result']) {
                    result_data = data['data'][0];
                    createEStandLineChart({
                        selector: 'chart_1558345623849', // 图表容器
                        data: result_data['disk_usage'], // 图表数据
                    });
                }
            }
        });
    });
```
**上段代码应该不能直接运行，我只是截取了一部分代码
需要你再修缮下，效果大致如下**

![front](https://smartpublic-10032816.file.myqcloud.com/custom/20190520220149/17266/20190520220149/--da8796ecb2174fdb1f73bf3b70d224fc.png)