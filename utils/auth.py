# !/usr/bin/env python
# -*- coding:utf-8 -*-
# API认证

import time
import hashlib
from AutoCMDB.settings import ASSET_AUTH_HEADER_NAME,ASSET_AUTH_KEY,ASSET_AUTH_TIME
from django.http import JsonResponse

# 已经访问过的列表 encrypt_list
ENCRYPT_LIST = [

]

def api_auth_method(request):
    # 从meta中获取头信息中key
    auth_key = request.META.get('HTTP_AUTH_KEY')
    if not auth_key:
        return False
    # 取出加密的秘钥和时间
    sp = auth_key.split('|')
    if len(sp) != 2:
        return False

    encrypt,timestamp = sp
    timestamp = float(timestamp)
    # 设置访问间隔超时时间
    limit_timestamp = time.time() - ASSET_AUTH_TIME
    # 判断是否超时
    if limit_timestamp > timestamp:
        return False

    # 不超时的情况下对秘钥进行验证
    ha = hashlib.md5(ASSET_AUTH_KEY.encode('utf-8'))
    ha.update(bytes('%s|%s' % (ASSET_AUTH_KEY,timestamp),encoding='utf-8'))
    result = ha.hexdigest()

    # 判断秘钥是否正确
    if encrypt != result:
        return False

    # 判断列表中是否已经访问记录 对已经失效的元素进行清除
    exist = False
    del_keys = []

    # 通过enumerate取出索引和值
    for k,v in enumerate(ENCRYPT_LIST):

        m = v['time']
        n = v['encrypt']

        if m < limit_timestamp:
            # 将已经超时的访问记录删除 根据索引来进行删除
            del_keys.append(k)
            continue
        if n == encrypt:
            exist = True

    for k in del_keys:
        del ENCRYPT_LIST[k]

    if exist:
        return False

    ENCRYPT_LIST.append({'encrypt':encrypt,'time':timestamp})

    return True

def api_auth(func):
    def inner(request,*args,**kwargs):
        if not api_auth_method(request):
            return JsonResponse({'code':1001,'message':'API授权失败'},json_dumps_params={'ensure_ascii':False})
        return func(request,*args,**kwargs)

    return inner