#!/usr/bin/env python
# -*- coding:utf-8 -*-


from methods_on_tiff import *
import time
# sharedPath = '/mnt/hgfs/Data/qhl'


#########################################
# 计算每月的fpar最大值，减少云雪及其他噪声的影响
# 输出名为2013_9_max.tiff形式的影像文件
#########################################

# 获取Fpar_1km文件列表
# fpar_files = getRasters(sharedPath, ['Fpar_1km'])
# st = time.time()
# max_monthly_fpar(sharedPath, fpar_files)
# et = time.time()
# print '计算MAX_Montly耗时：' + str(et - st) + ' s'

sharedPath = '/mnt/hgfs/Data/Fpar'

#########################################
# 计算每月的fpar最大值，减少云雪及其他噪声的影响
# 输出名为2013_9_max.tiff形式的影像文件
#########################################

# 获取Fpar_1km文件列表
st = time.time()
fpar_files = getRasters(sharedPath, ['Fpar_1km'])
files = []
temp = []
for i in range(len(fpar_files)):
    for k in range(len(fpar_files[i])):
        temp.append(fpar_files[i][k])
        files.append(temp)
        temp = []
max_monthly_fpar(sharedPath, files)
et = time.time()
print '计算MAX_Montly耗时：' + str(et - st) + ' s'


#########################################
# 计算DHI_CUM
# 输出名为2013_cum.tiff形式的影像文件
#########################################
# st = time.time()
# max_files = getRasters(sharedPath, ['max'])
# max_files.sort()
# DHI_cum(sharedPath, max_files)
# et = time.time()
# print '计算DHI_cum耗时：' + str(et - st) + ' s'

#########################################
# 计算DHI_MIN
# 输出名为2013_min.tiff形式的影像文件
#########################################
# st = time.time()
# max_files = getRasters(sharedPath, ['max'])
# max_files.sort()
# DHI_min(sharedPath, max_files)
# et = time.time()
# print '计算DHI_min耗时：' + str(et - st) + ' s'


#########################################
# 计算DHI_SEA
# 输出名为2013_sea.tiff形式的影像文件
#########################################
# st = time.time()
# cumfile = []
# cum = getRasters(sharedPath, ['cum'])
# for i in cum:
#     if i:
#         cumfile.append(i)
#     else:
#         continue
# for k in cumfile:
#     if k:
#         for n in range(len(k)):
#             year = k[n][-13:-9]
#             DHI_sea(sharedPath, year, k[n])
#     else:
#         continue
# et = time.time()
# print '计算DHI_sea耗时：' + str(et - st) + ' s'