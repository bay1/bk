# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class Host(models.Model):
    ip = models.GenericIPAddressField(max_length=30)
    system = models.CharField(max_length=64)
    disk = models.CharField(max_length=30)
    add_time = models.DateTimeField('录入时间', auto_now=True)
