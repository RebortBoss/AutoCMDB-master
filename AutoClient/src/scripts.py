# !/usr/bin/env python
# -*- coding:utf-8 -*-

from .client import AutoAgent,AutoSSH,AutoSalt
from AutoClient.config import settings

def client():
    if settings.MODE == 'agent':
        cli = AutoAgent()
    elif settings.MODE == 'ssh':
        cli = AutoSSH()
    elif settings.MODE == 'salt':
        cli = AutoSalt()
    else:
        raise Exception('请配置资产信息采集模式,如:ssh,agent,salt')

    cli.process()