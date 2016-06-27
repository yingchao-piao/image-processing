import gdal
import sys

# Read GeoTIFF images
try:
    tif = gdal.Open('filename.tif')
    tifArray = tif.ReadAsArray()
except:
    print 'The file does not exist.'
    sys.exit(0)
    