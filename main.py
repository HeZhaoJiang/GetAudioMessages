'''
Author: hezhaojiang
Date: 2021-07-19 10:21:12
LastEditTime: 2021-07-19 17:07:51
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \GetAudioMessages\main.py
'''
# -*- coding: utf-8 -*-

import os
import sys
import time
import gzip
import platform

if sys.version_info.major != 3:
    print('请使用Python3')
    exit(1)
try:
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)
adb = auto_adb()
VERSION = "1.0.0"

def gunzip(file_name):
    if -1 == file_name.find(".gz"):
        return
    name = file_name.replace(".gz", "")
    file = gzip.GzipFile(file_name)
    #读取解压后的文件，并写入去掉后缀名的同名文件（即得到解压后的文件）
    open(name, "wb+").write(file.read())
    file.close()
    os.remove(file_name)

def cat(file_src, file_dst):
    open(file_dst, 'ab+').write(open(file_src, 'rb').read())

def main():
    """
    主函数
    """
    print('程序版本号：{}'.format(VERSION))
    adb.select_device()
    dirname = adb.adb_device + time.strftime("_%Y%m%d%H%M%S",  time.localtime())
    print('日志输出到文件夹： {}'.format(dirname))
    if platform.system() == 'Windows':
        dirname = os.path.join(os.getcwd(), dirname)
    ## dirname = os.path.join(os.getcwd(), 'test')
    dirname_log = os.path.join(dirname, 'log')
    if not os.path.exists(dirname_log):
        os.makedirs(dirname_log)
    print(dirname)

    ## 获取文件
    adb.run('pull /data/log/ ' + dirname)
    adb.run('pull /var/log/messages ' + os.path.join(dirname_log, 'messages.-1'))

    ## 解压文件
    files = os.listdir(dirname_log)
    for file in files:
        if 0 != file.find("messages"):
            os.remove(os.path.join(dirname_log, file))
        else:
            gunzip(os.path.join(dirname_log, file))

    ## 排序 & 合并文件
    files = os.listdir(dirname_log)
    files.sort(key=lambda x:int(x.split('.')[1])) # messages.*
    for file in files[: :-1]:
        cat(os.path.join(dirname_log, file), os.path.join(dirname_log, "messages"))
        os.remove(os.path.join(dirname_log, file))

if __name__ == '__main__':
    try:
        main()
        print('\n谢谢使用')
        print('\nPlease Report Bugs to hezhaojiang@xiaomi.com.')
    except KeyboardInterrupt:
        print('\n谢谢使用')
        exit(0)
