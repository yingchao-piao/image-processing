# -*- coding:utf-8 -*-

###############################################################################
# 该模块定义了对modis fpar文件操作的方法
###############################################################################

import os
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
from osgeo import gdal
import numpy as np
from Convert import *


# 返回形式为 [['MCD15A3A2002185_Fpar_1km_MOD_Grid_MOD15A2.tif'],['MCD15A3A2002189_Fpar_1km_MOD_Grid_MOD15A2.tif']] 的文件索引
# 参数： folder为根目录，keywords为文件名的关键字
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


# 返回形式为 [['2002_cum.tiff'],['2003_cum.tiff']] 的文件索引
# 参数： folder为根目录，keywords为文件名的关键字
def getRastersByMultiKey(folder, keywords):
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
                    if j in str:
                        continue
                    else:
                        str = ''
                        break
                if not str == '':
                    temp.append(str)

        result.append(temp)

    return result


# 计算文件序列的最大值
# 参数： path输出的文件路径，period为monthly/annual，filesname为period内fpar的tiff文件列表
def max_fpar(path, period, filesname):
    maxArray = []
    for k in filesname:
        tif = gdal.Open(k)
        tifTemp = tif.ReadAsArray()
        tifArray = np.array(tifTemp)
        # 将影像中的无效值设置为NaN
        tifArray[tifArray >= 249] = np.nan

        if maxArray == []:
            maxArray.append(tifArray)
            maxArray = np.array(maxArray[0])
            # 将影像中的无效值设置为NaN
            maxArray[maxArray >= 249] = np.nan

            # Set outfile info
            outfilename = path + '/' + str(period) + '_max.tiff'
            # print outfilename
            image_format = 'GTiff'
            driver = gdal.GetDriverByName(image_format)
            # 将输出文件数据类型改为float，否则数值范围为0-255
            dsOut = driver.Create(outfilename, tif.RasterXSize, tif.RasterYSize, 1, GDT_Float64)
            dsOut.SetProjection(tif.GetProjection())
            dsOut.SetGeoTransform(tif.GetGeoTransform())
            bandOut = dsOut.GetRasterBand(1)

        else:
            maxArray = maxArray * (maxArray >= tifArray) + tifArray * (maxArray < tifArray)

    bandOut.WriteArray(maxArray)


# 计算文件序列的总和
# 参数： path输出的文件路径，period为month/annual，filesname为period内max_fpar的tiff文件列表


def cum_fpar(path, period, filesname):
    cumArray = []
    for k in filesname:
        tif = gdal.Open(k)
        tifTemp = tif.ReadAsArray()
        tifArray = np.array(tifTemp)
        if cumArray == []:
            cumArray.append(tifArray)
            cumArray = np.array(cumArray[0])

            # 配置输出文件信息
            outfilename = path + '/' + str(period) + '_cum.tiff'
            image_format = 'GTiff'
            driver = gdal.GetDriverByName(image_format)
            # 将输出文件数据类型改为float，否则数值范围为0-255
            dsOut = driver.Create(outfilename, tif.RasterXSize, tif.RasterYSize, 1, GDT_Float64)
            dsOut.SetProjection(tif.GetProjection())
            dsOut.SetGeoTransform(tif.GetGeoTransform())
            bandOut = dsOut.GetRasterBand(1)

        else:
            cumArray = cumArray + tifArray

    bandOut.WriteArray(cumArray)


# outpath = '/mnt/hgfs/Data/qhl/'
# filesname = [['/mnt/hgfs/Data/qhl/MCD15A3.005/MCD15A3A2002185/MCD15A3A2002185_Fpar_1km_MOD_Grid_MOD15A2.tif'],
#              ['/mnt/hgfs/Data/qhl/MCD15A3.005/MCD15A3A2002189/MCD15A3A2002189_Fpar_1km_MOD_Grid_MOD15A2.tif']]
# max_fpar(outpath, 'monthly', filesname)


# 计算文件序列的最小值
# 参数： path输出的文件路径，period为year，filesname为period内max_fpar的tiff文件列表

def min_fpar(path, period, filesname):
    minArray = []
    for k in filesname:
        tif = gdal.Open(k)
        tifTemp = tif.ReadAsArray()
        tifArray = np.array(tifTemp)
        if minArray == []:
            minArray.append(tifArray)
            minArray = np.array(minArray[0])

            # 配置输出文件信息
            outfilename = path + '/' + str(period) + '_min.tiff'
            image_format = 'GTiff'
            driver = gdal.GetDriverByName(image_format)
            # 将输出文件数据类型改为float，否则数值范围为0-255
            dsOut = driver.Create(outfilename, tif.RasterXSize, tif.RasterYSize, 1, GDT_Float64)
            dsOut.SetProjection(tif.GetProjection())
            dsOut.SetGeoTransform(tif.GetGeoTransform())
            bandOut = dsOut.GetRasterBand(1)

        else:
            minArray = minArray * (minArray <= tifArray) + tifArray * (minArray > tifArray)

    bandOut.WriteArray(minArray)

#########################################
# 计算每月的fpar最大值，减少云雪及其他噪声的影响
# 输出名为2013_9_max.tiff形式的影像文件
#########################################


def max_monthly_fpar(sharedPath, files):
    dict = {'year': [], 'month': [], 'filesname': []}

    for i in files:
        if i:
            file_date = date_of_modis(i[0])
            if not file_date[0] in dict['year']:
                if not dict['month'] == []:
                    period = str(dict['year'].pop()) + '_' + str(dict['month'].pop())
                    # print period
                    # print dict['filesname']
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
                    # print period
                    # print dict['filesname']
                    max_fpar(sharedPath, period, dict['filesname'])
                    dict['month'] = [file_date[1]]
                    dict['filesname'] = i
                else:
                    dict['filesname'].append(i[0])
        else:
            continue

#########################################
# 计算DHI_CUM
# 输出名为2013_cum.tiff形式的影像文件
#########################################


def DHI_cum(sharedPath, files):
    dict = {'year': [], 'filesname': []}
    for i in files:
        if i:
            for k in range(len(i)):
                year = i[k][-16:-12]
                # print year
                if year not in dict['year']:
                    if dict['year'] == []:
                        dict['year'] = year
                        dict['filesname'].append(i[k])
                    else:
                        period = str(dict['year'])
                        cum_fpar(sharedPath, period, dict['filesname'])
                        dict['year'] = year
                        dict['filesname'] = []
                        dict['filesname'].append(i[k])
                else:
                    dict['filesname'].append(i[k])
            cum_fpar(sharedPath, str(dict['year']), dict['filesname'])
        else:
            continue


#########################################
# 计算DHI_MIN
# 输出名为2013_cum.tiff形式的影像文件
#########################################


def DHI_min(sharedPath, files):
    dict = {'year': [], 'filesname': []}
    for i in files:
        if i:
            for k in range(len(i)):
                year = i[k][-16:-12]
                # print year
                if year not in dict['year']:
                    if dict['year'] == []:
                        dict['year'] = year
                        dict['filesname'].append(i[k])
                    else:
                        period = str(dict['year'])
                        min_fpar(sharedPath, period, dict['filesname'])
                        dict['year'] = year
                        dict['filesname'] = []
                        dict['filesname'].append(i[k])
                else:
                    dict['filesname'].append(i[k])
            min_fpar(sharedPath, str(dict['year']), dict['filesname'])
        else:
            continue


#########################################
# 计算DHI_SEA
# 计算avg = mean(Max_Monthly_Fpar)
# var = sum((max_mon-avg) **2) / num, num为月份个数
# std = sqrt(var)
# DHI_SEA = std/avg
#########################################
def DHI_sea(path, period, cum):
    max_mon = []
    cumtif = gdal.Open(cum)
    cumTemp = cumtif.ReadAsArray()
    cumArray = np.array(cumTemp) / 1.0

    mon = getRastersByMultiKey(path, [period, 'max'])
    for i in mon:
        if i:
            max_mon.append(i)
        else:
            continue
    max_mon = max_mon[0]

    # 计算年均值
    avgArray = cumArray/len(max_mon)

    # Set outfile info
    outfilename = path + '/' + str(period) + '_avg.tiff'
    # print outfilename
    image_format = 'GTiff'
    driver = gdal.GetDriverByName(image_format)
    # 将输出文件数据类型改为float，否则数值范围为0-255
    dsOut = driver.Create(outfilename, cumtif.RasterXSize, cumtif.RasterYSize, 1, GDT_Float64)
    dsOut.SetProjection(cumtif.GetProjection())
    dsOut.SetGeoTransform(cumtif.GetGeoTransform())
    bandOut = dsOut.GetRasterBand(1)
    bandOut.WriteArray(avgArray)

    # 计算年方差
    varArray = []
    for k in range(len(max_mon)):
        tif = gdal.Open(max_mon[k])
        tifTemp = tif.ReadAsArray()
        tifArray = np.array(tifTemp)
        tifArray[tifArray == 0] = np.nan
        s_Array = tifArray - avgArray
        # s_Array = np.array(s_Array)
        np.square(s_Array, out=s_Array)
        if varArray == []:
            s_Array.tolist()
            varArray = s_Array
            varArray = np.array(varArray)
        else:
            varArray = varArray + s_Array
    varArray /= len(max_mon)
    # Set outfile info
    outfilename = path + '/' + str(period) + '_var.tiff'
    # print outfilename
    image_format = 'GTiff'
    driver = gdal.GetDriverByName(image_format)
    # 将输出文件数据类型改为float，否则数值范围为0-255
    dsOut = driver.Create(outfilename, cumtif.RasterXSize, cumtif.RasterYSize, 1, GDT_Float64)
    dsOut.SetProjection(cumtif.GetProjection())
    dsOut.SetGeoTransform(cumtif.GetGeoTransform())
    bandOut = dsOut.GetRasterBand(1)
    bandOut.WriteArray(varArray)

    # 计算年标准差
    stdArray = varArray
    np.sqrt(varArray, out=stdArray)
    # Set outfile info
    outfilename = path + '/' + str(period) + '_std.tiff'
    # print outfilename
    image_format = 'GTiff'
    driver = gdal.GetDriverByName(image_format)
    # 将输出文件数据类型改为float，否则数值范围为0-255
    dsOut = driver.Create(outfilename, cumtif.RasterXSize, cumtif.RasterYSize, 1, GDT_Float64)
    dsOut.SetProjection(cumtif.GetProjection())
    dsOut.SetGeoTransform(cumtif.GetGeoTransform())
    bandOut = dsOut.GetRasterBand(1)
    bandOut.WriteArray(stdArray)


    # 计算DHI_sea
    seaArray = stdArray/avgArray
    # Set outfile info
    outfilename = path + '/' + str(period) + '_sea.tiff'
    # print outfilename
    image_format = 'GTiff'
    driver = gdal.GetDriverByName(image_format)
    # 将输出文件数据类型改为float，否则数值范围为0-255
    dsOut = driver.Create(outfilename, cumtif.RasterXSize, cumtif.RasterYSize, 1, GDT_Float64)
    dsOut.SetProjection(cumtif.GetProjection())
    dsOut.SetGeoTransform(cumtif.GetGeoTransform())
    bandOut = dsOut.GetRasterBand(1)
    bandOut.WriteArray(seaArray)

    print 'DHI_sea is finished!'


