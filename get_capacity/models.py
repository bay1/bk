from django.db import models


# Create your models here.
class DiskUsage(models.Model):
    ip = models.GenericIPAddressField(max_length=30, null=True, blank=False)
    system = models.CharField(max_length=64, null=True)
    mounted = models.CharField(max_length=30, null=True)
    value = models.IntegerField('磁盘使用率', null=True)
    add_time = models.DateTimeField('录入时间', auto_now=True)


class MemoryUsage(models.Model):
    value = models.IntegerField('内存使用率', null=True)
    add_time = models.DateTimeField('录入时间', auto_now=True)
