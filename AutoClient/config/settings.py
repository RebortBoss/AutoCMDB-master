# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 配置文件
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 用于API认证的KEY
KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'
# 用于API认证的请求头
AUTH_KEY_NAME = 'auth-key'

# 错误日志
ERROR_LOG_FILE = os.path.join(BASE_DIR,'log','error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASE_DIR,'log','run.log')

# Agent模式保存服务器唯一ID的文件
CERT_FILE_PATH = os.path.join(BASE_DIR,'config','cert')

# 是否是测试模式,测试模式从files目录下读取
TEST_MODE = True

# 采集资产的方式,agent(默认) salt ssh
MODE = 'agent'

# 如果采用ssh方式,则需要配置ssh的key和user
SSH_PRIVATE_KEY = '/home/auto/.ssh/id_rsa'
SSH_USER = 'root'
SSH_PORT = 22

# 采集硬件数据的插件
PLUGINS_DICT = {
    'cpu': 'AutoClient.src.plugins.cpu.CpuPlugin',
    'disk': 'AutoClient.src.plugins.disk.DiskPlugin',
    'main_board': 'AutoClient.src.plugins.main_board.MainBoardPlugin',
    'memory': 'AutoClient.src.plugins.memory.MemoryPlugin',
    'nic': 'AutoClient.src.plugins.nic.NicPlugin',
}

# 资产信息api
ASSET_API = 'http://127.0.0.1:8080/api/asset'
"""
POST时,返回值:{'code':xx,'message':'xx'}
    code:
        -- 1000 成功
        -- 1001 接口授权失败
        -- 1002 数据库中资产不存在
"""
