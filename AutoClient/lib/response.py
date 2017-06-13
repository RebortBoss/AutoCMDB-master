# !/usr/bin/env python
# -*- coding:utf-8 -*-

class BaseResponse:

    def __init__(self):
        self.status = True
        self.message = None
        self.data = None
        self.error = None