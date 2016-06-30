# -*- coding:utf-8 -*-

###############################################################################

###############################################################################

import os
import gdal
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

def max_monthly(filesname):
    maxArray = []
    XSize = 0
    YSize = 0
    for k in filesname:
        try:
            tif = gdal.Open(k[0])
            band = tif.GetRasterBand(1)
            XSize = tif.RasterXSize
            YSize = tif.RasterYSize
            tifTemp = tif.ReadAsArray()
            tifArray = np.array(tifTemp)
            if maxArray == []:
                maxArray.append(tifArray)
                maxArray = np.array(maxArray[0])
            else:
                maxArray = maxArray * (maxArray >= tifArray) + tifArray * (maxArray < tifArray)
        except:
            print k[0] + ' does not exist.'
    return maxArray, band.DataType, XSize, YSize



def write_tiff(outpath, tifArray, dataType, XSize, YSize):
    dst_filename = outpath + 'test.tiff'
    image_format = 'GTiff'
    driver = gdal.GetDriverByName(image_format)
    dst_ds = driver.Create(dst_filename, XSize, YSize, 1, dataType)
    dst_ds.GetRasterBand(1).WriteArray(tifArray, 0, 0)
    dst_ds = None

    return dst_filename

outpath='/mnt/hgfs/Data/qhl/'
filesname = [['/mnt/hgfs/Data/qhl/MCD15A3.005/MCD15A3A2002185/MCD15A3A2002185_Fpar_1km_MOD_Grid_MOD15A2.tif'],
             ['/mnt/hgfs/Data/qhl/MCD15A3.005/MCD15A3A2002189/MCD15A3A2002189_Fpar_1km_MOD_Grid_MOD15A2.tif']]
[a, datatype, x, y] = max_monthly(filesname)
print a, datatype, x, y
write_tiff(outpath, a, datatype, x, y)





