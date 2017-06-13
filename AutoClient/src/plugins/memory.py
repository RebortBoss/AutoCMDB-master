# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import traceback
from AutoClient.lib import convert
from .base import BasePlugin
from AutoClient.lib.response import BaseResponse


class MemoryPlugin(BasePlugin):
    '''
    内存信息
    '''
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_mode:
                from AutoClient.config.settings import BASE_DIR
                output = open(os.path.join(BASE_DIR,'files/memory.out'),'r').read()

            else:
                shell_command = 'sudo dmidecode -q -t 17 2>/dev/null'
                output = self.exec_shell_cmd(shell_command)

            response.data = self.parse(output)
        except Exception as e:
            msg = '%s linux memory plugin error: %s'
            self.logger.log(msg % (self.hostname,traceback.format_exc()),False)
            response.status = False
            response.error = msg % (self.hostname,traceback.format_exc())

        return response


    def parse(self,content):
        '''
        解析shell命令
        :param content:
        :return:
        '''
        ram_dict = {}
        key_map = {
            'Size': 'capacity',
            'Locator': 'slot',
            'Type': 'model',
            'Speed': 'speed',
            'Manufacturer': 'manufacturer',
            'Serial Number': 'sn',
        }

        devices = content.split('Memory Device')
        for item in devices:
            item = item.strip()
            if not item:
                continue
            if item.startswith('#'):
                continue
            segment = {}
            lines = item.split('\n\t')

            for line in lines:
                if len(line.split(':')) > 1:
                    key,value = line.split(':')

                else:
                    key = line.split(':')[0]
                    value = ""

                if key in key_map:
                    if key == 'Size':
                        segment[key_map['Size']] = convert.convert_mb_to_gb(value,0)
                    else:
                        segment[key_map[key.strip()]] = value.strip()

            ram_dict[segment['slot']] = segment


        return ram_dict