from django.shortcuts import render,HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from utils import auth
from api.service import asset
from repository import models

class AssetView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AssetView,self).dispatch(request,*args,**kwargs)

    @method_decorator(auth.api_auth)
    def get(self,request,*args,**kwargs):
        '''
        获取今日未更新的资产 - 用于SSH或Salt客户端
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        response = asset.get_untreated_servers()
        return JsonResponse(response.__dict__)

    @method_decorator(auth.api_auth)
    def post(self,request,*args,**kwargs):
        '''
        更新或者添加资产信息
        :param request:
        :param args:
        :param kwargs:
        :return: 1000 成功,1001 接口授权失败,1002 数据库中资产不存在
        '''

        # 将字节变成字符串
        server_info = json.loads(request.body.decode('utf-8'))
        # 将字节变成json类型
        server_info = json.loads(server_info)

        hostname = server_info['hostname']

        ret = {
            'code':1000,
            'message':'[%s]更新完成' % hostname
        }

        # 根据主机名去数据库获取相关信息
        server_obj = models.Server.objects.filter(hostname=hostname).select_related('asset').first()

        if not server_obj:
            ret['code'] = 1002
            ret['message'] = '[%s]资产不存在' % hostname
            return JsonResponse(ret)

        return JsonResponse(ret)