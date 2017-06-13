# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import hashlib
import requests
import time
from AutoClient.src import plugins
from AutoClient.lib.log import Logger
from AutoClient.lib.serialize import Json
from AutoClient.config import settings

from concurrent.futures import ThreadPoolExecutor

class AutoBase:
    def __init__(self):
        self.asset_api = settings.ASSET_API
        self.key = settings.KEY
        self.key_name = settings.AUTH_KEY_NAME

    def auth_key(self):
        '''
        接口认证
        :return:
        '''
        ha = hashlib.md5(self.key.encode('utf-8'))      # 加盐
        time_span = time.time()
        # 将日期和key一起加密
        ha.update(bytes('%s|%f' % (self.key,time_span),encoding='utf-8'))
        encryption = ha.hexdigest()

        # 将加密的结果和加密的时间一起返回
        result = '%s|%f' % (encryption,time_span)

        return {self.key_name:result}

    def get_asset(self):
        '''
        通过get的方式获取资产
        :return: {"data": [{"hostname": "c1.com"}, {"hostname": "c2.com"}], "error": null, "message": null, "status": true}
        '''

        try:
            header = {}
            header.update(self.auth_key())
            # 提交数据的时候,将认证添加请求头
            response = requests.get(
                url=self.asset_api,
                headers=header
            )
        except Exception as e:
            response = e
        print("服务端获取数据===>",response.json())
        return response.json()

    def post_asset(self,msg,callback=None):
        '''
        post方式提交资产
        :param msg:
        :param callback:
        :return:
        '''
        status = True
        try:
            header = {}
            header.update(self.auth_key())
            response = requests.post(
                url=self.asset_api,
                headers=header,
                json=msg
            )

        except Exception as e:
            print('异常',e)
            response = e
            status = False

        if callback:
            callback(status,response)

        print("服务端返回的结果===>",json.loads(response.text))

    def process(self):
        '''
        子类需要继承此方法,用于处理请求的入口
        :return:
        '''
        raise NotImplementedError('you must implement process method')

    def callback(self,status,response):
        '''
        提交资产后的回调函数
        :param status: 是否请求成功
        :param response: 请求成功,则是响应内容对象,请求错误,则是异常对象
        :return:
        '''
        if not status:
            Logger().log(str(response),False)
            return

        ret = json.loads(response.text)

        if ret['code'] == 1000:
            # True 表示运行日志
            Logger().log(ret['message'],True)
        else:
            # False 表示错误日志
            Logger().log(ret['message'],False)

class AutoAgent(AutoBase):
    '''
    agent形式
    '''
    def __init__(self):
        self.cert_file_path = settings.CERT_FILE_PATH
        super(AutoAgent,self).__init__()

    def load_local_cert(self):
        '''
        获取本地标识
        :return:
        '''
        if not os.path.exists(self.cert_file_path):
            # 文件不存在的情况返回None
            return None
        with open(self.cert_file_path,mode='r') as f:
            data = f.read()
        if not data:
            # 没有数据的情况也返回None
            return None
        cert = data.strip()
        return cert

    def write_local_cert(self,cert):
        '''
        写入本地标识
        :param cert:
        :return:
        '''
        if not os.path.exists(self.cert_file_path):
            os.makedirs(os.path.basename(self.cert_file_path))
        with open(self.cert_file_path,mode='w') as f:
            f.write(cert)

    def process(self):
        '''
        获取当前资产信息
        1.在资产中获取主机名 cert_new
        2.在本地cert文件中获取主机名 cert_old
        如果cert文件中为空,表示是新的资产
            - 则将 cert_new 写入该文件中,发送数据到服务器(新资产)
        如果两个名称不相等
            - 如果db=new,则,表示应该主动修改,new为唯一id

        :return:
        '''

        server_info = plugins.get_server_info()
        # 如果获取服务器信息失败,直接返回
        if not server_info.status:
            return

        # 加载本地的cert
        local_cert = self.load_local_cert()
        if local_cert:
            if local_cert == server_info.data['hostname']:
                # 说明主机名相等
                # 不做操作
                pass
            else:
                server_info.data['hostname'] = local_cert
        else:
            # 将主机名写入本地
            self.write_local_cert(server_info.data['hostname'])

        server_json = Json.dumps(server_info.data)

        # 测试get方法
        # self.get_asset()
        ###############
        # post提交,提交成功,将数据写入日志
        self.post_asset(server_json,self.callback)

class AutoSSH(AutoBase):
    '''
    ssh模式
    '''
    def process(self):
        '''
        根据主机名获取资产信息,将其发送到api
        通过get的形式获取
        :return:
        '''
        task = self.get_asset()
        # 获取失败的话,写入错误日志
        if not task['status']:
            Logger().log(task['message'],False)

        # 通过线程池来提交数据
        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run,hostname)

        pool.shutdown(wait=True)

    def run(self,hostname):
        server_info = plugins.get_server_info(hostname)
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json,self.callback)

class AutoSalt(AutoBase):
    '''
    saltstack模式
    '''
    def process(self):
        '''
        根据主机名获取资产信息,将其发送的API
        :return:
        {
           "data": [ {"hostname": "c1.com"}, {"hostname": "c2.com"}],
           "error": null,
           "message": null,
           "status": true
        }
        '''
        task = self.get_asset()
        if not task['status']:
            Logger().log(task['message'],False)
        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run,hostname)

        pool.shutdown(wait=True)

    def run(self,hostname):
        '''
        获取指定主机名资产信息
        :param hostname:
        :return:
        '''
        server_info = plugins.get_server_info(hostname)
        # 序列化字符串
        server_json = Json.dumps(server_info.data)
        # 将数据发送到API
        self.post_asset(server_json,self.callback)


