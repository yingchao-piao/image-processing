#!/usr/bin/env python
# -*- coding:utf-8 -*-

###############################################################################

###############################################################################
from methods_on_tiff import *
from Convert import *
import time

st = time.time()
# 获取Fpar_1km文件列表
sharedPath = '/mnt/hgfs/Data/qhl'
result = getRasters(sharedPath, ['Fpar_1km'])

dict = {'year': [], 'month': [], 'filesname': []}

for i in result:
    if i:
        file_date = date_of_modis(i[0])
        if not file_date[0] in dict['year']:
            if not dict['month'] == []:
                period = str(dict['year'].pop()) + '_' + str(dict['month'].pop())
                print period
                print dict['filesname']
                max_fpar(sharedPath, period, dict['filesname'])
                dict['year'] = [file_date[0]]
                dict['month'] = [file_date[1]]
                dict['filesname'] = i
            else:
                dict['year'] = [file_date[0]]
                dict['month'] = [file_date[1]]
                dict['filesname'] = i
        else:
            if not file_date[1] in dict['month']:
                period = str(dict['year'][0]) + '_' + str(dict['month'].pop())
                print period
                print dict['filesname']
                max_fpar(sharedPath, period, dict['filesname'])
                dict['month'] = [file_date[1]]
                dict['filesname'] = i
            else:
                dict['filesname'].append(i[0])
    else:
        continue
et = time.time()
print '计算MAX_Montly耗时：' + str(et - st) + ' s'

