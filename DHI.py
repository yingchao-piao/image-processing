#!/usr/bin/env python
# -*- coding:utf-8 -*-

###############################################################################

###############################################################################
import gdal
from methods_on_tiff import *
from Convert import *

# 获取Fpar_1km文件列表
sharedPath = '/mnt/hgfs/Data/qhl'
result = getRasters(sharedPath, ['Fpar_1km'])

for i in result:
    if i:
        print i[0]
        # Find the date of the tiff file
        date_of_file = date_of_modis(i[0])
        print date_of_file
        try:
            tif = gdal.Open(i[0])
            tifArray = tif.ReadAsArray()
        except:
            print i[0] + ' does not exist.'
    else:
        continue
