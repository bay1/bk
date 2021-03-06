# -*- coding: utf-8 -*-
"""testapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from home_application import views

urlpatterns = (
    url(r'^$', views.home),
    url(r'^hello_world/$', views.hello),
    url(r'^host_disk/$', views.host_disk),
    url(r'^get_host_ips/$', views.get_host_ip),
    url(r'^add_host/$', views.add_host),
    url(r'^search_host/$', views.search_host),
    url(r'^api/get_dfusage_bay1/$', views.api_disk_usage),
    url(r'^get_cchost_ips/$', views.get_cchost_ips)
)
