#-*- coding: utf-8 -*-
import os, sys
reload(sys)
sys.setdefaultencoding('utf8')
import arcpy

arcpy.env.workspace = "E:/Work/Data"
gdb = "E:/Work/Data/辽宁省2006.gdb"
arcpy.env.overwriteOutput = True 
desc = arcpy.Describe(gdb)
domains = desc.domains
     
for domain in domains:   
    table = os.path.join(gdb, domain)
    arcpy.DomainToTable_management(gdb, domain, table, 'code','description', '#')    
