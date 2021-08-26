# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re
import subprocess
import platform


class auto_adb(object):
    def __init__(self):
        try:
            adb_path = 'adb'
            subprocess.Popen([adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.adb_path = adb_path
        except OSError:
            if platform.system() == 'Windows':
                adb_path = os.path.join(os.getcwd(), 'tools', 'adb.exe')
                print(adb_path)
                try:
                    subprocess.Popen([adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.adb_path = adb_path
                    return
                except OSError:
                   pass
            else:
                try:
                    subprocess.Popen(
                        [adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except OSError:
                    pass
            print('请安装 ADB 及驱动并配置环境变量')
            print('参考链接: https://www.xda-developers.com/install-adb-windows-macos-linux/')
            exit(1)

    def select_device(self):
        print('检查 adb 设备 ...')
        command_list = [self.adb_path, 'devices']
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        info = output[0].decode('utf8')
        if platform.system() == 'Windows':
            device_info = info.split('\r\n')
        else:
            device_info = info.split('\n')
        if device_info[1] == '':
            print('未找到设备')
            print('adb 输出:')
            for each in output:
                print(each.decode('utf8'))
            exit(1)
        index = 0
        for each in device_info:
            if index != 0 and device_info[index] != "":
                print("{}.  {}".format(index, device_info[index]))
            index = index + 1
        while 1:
            try:
                index = int(input("请输入序号选择设备: "))
                self.adb_device = device_info[index].split('\t')[0]
                return
            except:
                pass

    def run(self, raw_command):
        command = '{} -s {} {}'.format(self.adb_path, self.adb_device, raw_command)
        process = os.popen(command)
        output = process.read()
        return output

    def adb_path(self):
        return self.adb_path
