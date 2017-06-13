# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from web.service import asset
from django.views import View

class AssetListView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'asset_list.html')

class AssetJsonView(View):
    def get(self,request):
        """
        获取资产数据
        :param request:
        :return:
        """
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self,request):
        """
        删除资产
        :param request:
        :return:
        """
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self,request):
        """
        更新资产
        :param request:
        :return:
        """
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)

class AssetDetailView(View):
    """
    资产详情
    """
    def get(self,request,device_type_id,asset_nid):
        response = asset.Asset.assets_detail(device_type_id,asset_nid)
        return render(request,'asset_detail.html',{'response': response, 'device_type_id': device_type_id})

class AddAssetView(View):
    """
    添加资产
    """
    def get(self,request,*args,**kwargs):
        return render(request,'add_asset.html')


class IDCListView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'idc_list.html')


class IDCJsonView(View):
    def get(self,request):
        pass

    def delete(self,request):
        pass

    def put(self,request):
        pass
