# -*- coding:utf-8 -*-

###############################################################################

###############################################################################

import os
import gdal


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

