# -*- coding:utf-8 -*-


from methods_on_tiff import *
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def makeThumbnail(src):
    dataset = gdal.Open(src)

    # 判断数据集的波段数
    if (dataset.RasterCount < 1):
        return
    if (dataset.RasterCount > 1):
        ds = dataset.GetRasterBand(1).ReadAsArray()
    else:
        ds = dataset.ReadAsArray()

    A = np.array(ds)
    fig = plt.figure(frameon=False)  # 生成画布
    ax = fig.add_subplot(111)  # 增加子图
    ax.imshow(A, interpolation='nearest', vmin=0, vmax=100, cmap=plt.cm.gist_earth)  # 子图上显示数据
    plt.savefig(src.replace('.tiff', '.THUMBNAIL.png'), dpi=80)
    ax.set_xticks([])  # 去除坐标轴
    ax.set_yticks([])
    plt.savefig(src.replace('.tiff', '.png'), dpi=300)
    ds = None
    dataset = None

sharedPath = '/mnt/hgfs/Data/DHI_20160705'
files = getRasters(sharedPath, ['min'])[0]

for i in range(len(files)):
    makeThumbnail(files[i])
