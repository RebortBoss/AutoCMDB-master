# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import os
import traceback
from .base import BasePlugin
from AutoClient.lib.response import BaseResponse

class NicPlugin(BasePlugin):
    '''
    网卡信息
    '''

    def linux(self):
        response = BaseResponse()
        try:
            if self.test_mode:
                from AutoClient.config.settings import BASE_DIR
                output = open(os.path.join(BASE_DIR, 'files/nic.out'), 'r').read()
                interfaces_info = self._interfaces_ip(output)
            else:
                interfaces_info = self.linux_interfaces()

            self.standard(interfaces_info)
            response.data = interfaces_info

        except Exception as e:
            msg = "%s linux nic plugin error: %s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())

        return response



    def linux_interfaces(self):
        '''
        获得*nix/BSD接口信息
        :return:
        '''
        ifaces = dict()
        ip_path = 'ip'
        if ip_path:
            cmd1 = self.exec_shell_cmd('sudo {0} link show'.format(ip_path))
            cmd2 = self.exec_shell_cmd('sudo {0} addr show'.format(ip_path))
            ifaces = self._interfaces_ip(cmd1 + '\n' + cmd2)

        return ifaces

    def _interfaces_ip(self,out):
        '''
        根据ip返回相关信息,比如上下线状态,ip地址,子网掩码等
        :param out:
        :return:
        '''
        ret = dict()
        right_keys = ['name', 'hwaddr', 'up', 'netmask', 'ipaddrs']

        def parse_network(value,cols):
            '''
            解析当前的网络状态
            :param value:
            :param cols:
            :return:
            '''
            brd = None
            mask = None
            if '/' in value:
                ip,cidr = value.split('/')
            else:
                ip = value
                cidr = 32
            if type_ == 'inet':
                mask = self.cidr_to_ipv4_netmask(int(cidr))
                if 'brd' in cols:
                    brd = cols[cols.index('brd') + 1]
            return (ip,mask,brd)

        groups = re.compile('\r?\n\\d').split(out)
        for group in groups:
            iface = None
            data = dict()

            for line in group.splitlines():
                if ' ' not in line:
                    continue
                match = re.match(r'^\d*:\s+([\w.\-]+)(?:@)?([\w.\-]+)?:\s+<(.+)>', line)
                if match:
                    iface,parent,attrs = match.groups()
                    if 'UP' in attrs.split(','):
                        data['up'] = True
                    else:
                        data['up'] = False

                    if parent and parent in right_keys:
                        data[parent] = parent

                    continue

                cols = line.split()
                if len(cols) >= 2:
                    type_,value = tuple(cols[0:2])
                    iflabel = cols[-1:][0]
                    if type_ in ('inet',):
                        if 'secondary' not in cols:
                            ipaddr,netmask,broadcast = parse_network(value,cols)
                            if type_ == 'inet':
                                if 'inet' not in data:
                                    data['inet'] = list()
                                addr_obj = dict()
                                addr_obj['address'] = ipaddr
                                addr_obj['netmask'] = netmask
                                addr_obj['broadcast'] = broadcast
                                data['inet'].append(addr_obj)
                        else:
                            if 'secondary' not in data:
                                data['secondary'] = list()
                            ip_,mask,brd = parse_network(value,cols)
                            data['secondary'].append({
                                'type':type_,
                                'address':ip_,
                                'netmask':mask,
                                'broadcast':brd,
                            })
                            del ip_,mask,brd
                    elif type_.startswith('link'):
                        data['hwaddr'] = value

            if iface:
                if iface.startswith('pan') or iface.startswith('lo') or iface.startswith('v'):
                    del iface,data
                else:
                    ret[iface] = data
                    del iface,data

        return ret

    def cidr_to_ipv4_netmask(self,cidr_bits):
        try:
            cidr_bits = int(cidr_bits)
            if not 1 <= cidr_bits <= 32:
                return ''
        except ValueError:
            return ''

        netmask = ''
        for idx in range(4):
            if idx:
                netmask += '.'
            if cidr_bits >= 8:
                netmask += '255'
                cidr_bits -= 8
            else:
                netmask += '{0:d}'.format(256 - (2 ** (8 - cidr_bits)))
                cidr_bits = 0

        return netmask

    def standard(self,interfaces_info):

        for key,value in interfaces_info.items():
            ipaddrs = set()
            netmask = set()
            if not 'inet' in value:
                value['ipaddrs'] = ''
                value['netmask'] = ''
            else:
                for item in value['inet']:
                    ipaddrs.add(item['address'])
                    netmask.add(item['netmask'])

                value['ipaddrs'] = '/'.join(ipaddrs)
                value['netmask'] = '/'.join(netmask)
                del value['inet']