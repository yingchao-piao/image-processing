#!/usr/bin/env python
# -*- coding:utf-8 -*-

###############################################################################

###############################################################################
import gdal
from methods_on_tiff import *

#获取Fpar_1km文件列表
sharedPath='/mnt/hgfs/Data/qhl'
result = getRasters(sharedPath, ['Fpar_1km'])

for i in result:
    if i:
        try:
            tif = gdal.Open(i[0])
            tifArray = tif.ReadAsArray()
        except:
            print i[0] + ' does not exist.'
    else:
        continue
