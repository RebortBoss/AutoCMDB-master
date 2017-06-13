# !/usr/bin/env python
# -*- coding:utf-8 -*-

from django.views import View
from django.shortcuts import render

class UserListView(View):
    def get(self,request,*agrs,**kwargs):

        return render(request,'users_list.html')