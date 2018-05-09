#-*- coding: utf-8 -*-
import os, sys
import arcpy
import csv
reload(sys)
sys.setdefaultencoding('utf8')

arcpy.env.workspace = "E:/Work/Data"
gdb = "E:/Work/Data/辽宁省2006.gdb"
arcpy.env.overwriteOutput = True 

featureclass = gdb + "/" + "J2210000JB2006XBM"
fields = arcpy.ListFields(featureclass)
field_domain =[]

for f in fields:        
    field_domain.append([f.name, f.domain])   

with open('results.csv','wb') as f:
    w = csv.writer(f)
    for row in field_domain:
        w.writerow([item.encode('utf8') for item in row])