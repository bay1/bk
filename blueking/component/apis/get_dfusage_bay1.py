# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsGetDfusageBay1(object):
    """Collections of get_dfusage_bay1 APIS"""

    def __init__(self, client):
        self.client = client

        self.get_dfusage_bay1 = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/self-service-api/api/get_dfusage_bay1/',
            description=u'获取指定磁盤容量'
        )
