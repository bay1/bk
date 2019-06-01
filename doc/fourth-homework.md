Base: Windows + Python 3.6 + 蓝鲸框架2.0

#### [Windows安装RabbitMQ环境](https://blog.csdn.net/tjcyjd/article/details/77150893)

#### config配置

>检查你的config中数据库等是否设置，确认消息队列采用了RabbitMQ

```python
# Celery 消息队列设置 RabbitMQ
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# Celery 消息队列设置 Redis
# BROKER_URL = 'redis://localhost:6379/0'
```

#### 简单celery任务 

>get_capacity 新建 celery_tasks.py，由于我们需要一个周期性的task
我们不需要构建相应的url，简单的示例可以如下：

```python
# -*- coding: utf-8 -*-
import logging
import datetime

from celery import task
from celery.task import periodic_task

logger = logging.getLogger('celery')

@task()
def get_capacity_task():
    """
    定义一个获取磁盘使用率异步任务
    """
    logger.info('disk usage work end')


@periodic_task(run_every=datetime.timedelta(seconds=1))
def get_disk_periodic():
    """
    获取磁盘使用率周期执行定义
    """
    get_capacity_task.delay()
    logger.info('get disk work starting')
```

>这个简单的示例代码，编写完成后，打开三个终端分别运行

```bash
python manage.py runserver
python manage.py celery worker -l info
python manage.py celery beat -l info # 周期任务需要这个命令
```

>如果终端输出正常，即每隔一秒打logger,证明你成功了
>下面截图是我当时备份，你的结果应该不一样，但每隔1s会有两个info输出

![celery](https://smartpublic-10032816.file.myqcloud.com/custom/20190516230809/17266/20190516230809/--be0697825b2ed3facaa2744f8ef40309.png)

#### 构建云API,client请求

```python
import base64

def base64_encode(string):
    """
    对字符串进行base64编码
    """
    return base64.b64encode(string).decode("utf-8")
```

>上段这段代码，你可以用来base64编码命令，因为快速执行脚本参数需要编码

```python
from blueapps.account.models import User
from blueking.component.shortcuts import get_client_by_user

user = User.objects.get(username=xxx)
client = get_client_by_user(user.username) # 这里是周期任务，不能通过request请求client

script_content = base64_encode(b"df -h ${1} | awk '{if(+$5&gt;0) print +$5}'")
script_param = base64_encode(b'/')
ip = xxxx

def fast_execute_script(client, script_content, script_param, ip):
    """
    快速执行脚本函数
    """
    kwargs = {
		xxxx # 具体参数看文档
    }
    return client.job.fast_execute_script(kwargs)
```

>利用base64函数，我们执行快速脚本API就可以这样
>其中kwargs中的，"bk_biz_id"，即业务ID 后台链接中可以查看,也可以通过API查询

[API网关调用说明](https://docs.bk.tencent.com/esb/APIspecification.html#APIcall)
[快速执行脚本文档](http://paas.class.o.qcloud.com/esb/api_docs/system/job/get_job_instance_log/)

** 你如果执行成功的话，在公共社区后台，作业执行历史是能够看到你的执行记录的**

![作业执行日志.png](https://smartpublic-10032816.file.myqcloud.com/custom/20190524125749/17266/20190524125749/--12bec2b759a0f14d9b06d329932d9794.png)

#### 然后我们为了获取执行结果需要调用另一个API接口，即作业执行日志查询
 
```python
def get_job_instance_log(client, job_instance_id):
    """
    对作业执行具体日志查询函数
    """

    kwargs = {
	xxx
    }
    time.sleep(2)  # todo 延时2s, 快速执行脚本需要一定的时间， 后期可以用celery串行两个函数
    return client.job.get_job_instance_log(kwargs)
```

**然后刚才快速执行被执行成功后，检测回显，如果message为success执行日志查询**

```python
# 如果快速脚本调用成功，执行log日志查询，获取执行内容
if fast_execute_script_result['message'] == 'success':
   job_instance_id = fast_execute_script_result['data']['job_instance_id']
   get_job_instance_log_result = get_job_instance_log(client, job_instance_id)

   # 如果日志查询成功，提取内容
   if get_job_instance_log_result['message'] == 'success':
       # 匹配log_content规则
       regex = r"(?&lt;='log_content': ').*?(?=')"

       return re.findall(regex, str(get_job_instance_log_result), re.MULTILINE)
   else:
       return None
```

#### 上面大概还介绍了所有或许用到的代码，没有直接贴完整的，需要你自己组装一下，获取了数据
我们可以通过Django的models把我们需要的数据存到数据库，比如磁盘使用率

```python
# 相应数据库可以参照
class DiskUsage(models.Model):
    value = models.IntegerField('磁盘使用率')
    add_time = models.DateTimeField('录入时间', auto_now=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="DiskUsage") # 如果你没有外键Host注释 这句

```

```python
def model_data_format(usages):
    usage_add_time = []
    usage_value = []
    for usage in usages:
        usage_add_time.append(usage.add_time.strftime("%Y/%m/%d %H:%M:%S"))
        usage_value.append(usage.value)
    return usage_add_time, usage_value

def api_disk_usage(request):
    """
    磁盘使用率API接口
    """
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

==============================
url(r'^get_dfusage_xx/$', views.api_disk_usage), # 然后配置相应url
```

**关于前端的展示，我们可以用https://magicbox.bk.tencent.com/ 拖拽两个折线图
只需要后端组装折线图需要的json数据就行了，就是上面的接口返回**

```js
   $(function(){
            initEStandLineChart({
                url: '', // 后端api接口，magicbox拖拽，只需要改这个
                dataType: 'json',
                containerId: 'chart_1558345625982'
            });   
    });
```

![front](https://smartpublic-10032816.file.myqcloud.com/custom/20190517111852/17266/20190517111852/--7a923b070c582cb11c8ac6ba3243c560.png)

>上面只是列举了部分函数，具体代码可以查看本仓库
>很多地方只是完成了功能，可能用户体验不太好