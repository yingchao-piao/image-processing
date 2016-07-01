# -*- coding:utf-8 -*-

###############################################################################

###############################################################################

import os
from osgeo.gdalnumeric import *
import numpy as np


##返回形式为 [['MCD15A3A2002185_Fpar_1km_MOD_Grid_MOD15A2.tif'],['MCD15A3A2002189_Fpar_1km_MOD_Grid_MOD15A2.tif']] 的文件索引
##参数： folder为根目录，keywords为文件名的关键字
def getRasters(folder, keywords):
    result = []
    for root, dirs, files in os.walk(folder):
        # 只有显示二级目录
        if files == []:
            continue
        else:
            temp = []
            # 连接文件名
            for name in files:
                str = os.path.join(root, name)
                # 根据关键字过滤
                for j in keywords:
                    if j in str and 'png' not in str:
                        temp.append(str)
                        break
        result.append(temp)

    return result


##计算文件序列的最大值
# 参数： path输出的文件路径，period为monthly/annual，filesname为period内fpar的tiff文件列表
def max_fpar(path, period, filesname):
    maxArray = []
    for k in filesname:
        tif = gdal.Open(k)
        tifTemp = tif.ReadAsArray()
        tifArray = np.array(tifTemp)
        if maxArray == []:
            maxArray.append(tifArray)
            maxArray = np.array(maxArray[0])

            # Set outfile info
            band = tif.GetRasterBand(1)
            outfilename = path + '/' + str(period) + '_max.tiff'
            print outfilename
            image_format = 'GTiff'
            driver = gdal.GetDriverByName(image_format)
            dsOut = driver.Create(outfilename, tif.RasterXSize, tif.RasterYSize, 1, band.DataType)
            CopyDatasetInfo(tif, dsOut)
            bandOut = dsOut.GetRasterBand(1)

        else:
            maxArray = maxArray * (maxArray >= tifArray) + tifArray * (maxArray < tifArray)
    maxArray.tolist()
    BandWriteArray(bandOut, maxArray)

##计算文件序列的总和
# 参数： path输出的文件路径，period为month/annual，filesname为period内fpar的tiff文件列表
def cum_fpar(path, period, filesname):
    cumArray = []
    for k in filesname:
        tif = gdal.Open(k)
        tifTemp = tif.ReadAsArray()
        tifArray = np.array(tifTemp)
        if cumArray == []:
            cumArray.append(tifArray)
            cumArray = np.array(cumArray[0])

            # Set outfile info
            band = tif.GetRasterBand(1)
            outfilename = path + '/' + str(period) + '_cum.tiff'
            image_format = 'GTiff'
            driver = gdal.GetDriverByName(image_format)
            dsOut = driver.Create(outfilename, tif.RasterXSize, tif.RasterYSize, 1, band.DataType)
            CopyDatasetInfo(tif, dsOut)
            bandOut = dsOut.GetRasterBand(1)

        else:
            cumArray = cumArray + tifArray
        cumArray.tolist()
    BandWriteArray(bandOut, cumArray)


# outpath = '/mnt/hgfs/Data/qhl/'
# filesname = [['/mnt/hgfs/Data/qhl/MCD15A3.005/MCD15A3A2002185/MCD15A3A2002185_Fpar_1km_MOD_Grid_MOD15A2.tif'],
#              ['/mnt/hgfs/Data/qhl/MCD15A3.005/MCD15A3A2002189/MCD15A3A2002189_Fpar_1km_MOD_Grid_MOD15A2.tif']]
# max_fpar(outpath, 'monthly', filesname)
