'''
Created on 2018年5月3日
dbf文件批量导入postgresql数据库
@author: piaopiao
'''

import psycopg2
import os
from pinyinutil import *

#连接数据库
conn = psycopg2.connect(database="liaoning",user="postgres",password="472594-piao",host="localhost",port=5432)
cur = conn.cursor()
cur.execute("SET CLIENT_ENCODING TO 'utf8';")

#创建属性域schema
query = 'CREATE SCHEMA IF NOT EXISTS domain AUTHORIZATION postgres;'
cur.execute(query)

#shp2pgsql执行文件所在目录（路径有空格，需双引号包含）
shp2pgsql_path = r'"C:\Program Files\PostgreSQL\10\bin\shp2pgsql"'

#dbf文件遍历
root = "E:\Work\Data"
for root, dirs, files in os.walk(root):
    for name in files:
        if(name.endswith(".dbf")):            
            in_table  = os.path.join(root,name)
            
            #导入数据库的table名称需小写字母，中文字符转拼音小写
            out_table = 'domain.' + to_pinyin(str(name[:-4])) 
            
            #shp2pgsql导出sql语句文件
            shp2pgsql_cmd= r'%s -s 4214 -d -n %s %s > %s' % (shp2pgsql_path, in_table, out_table, os.path.join(os.getcwd(),"import.sql"))            
            os.system(shp2pgsql_cmd)            
            print("import.sql is updated!\n")
            
            #执行导入数据的sql语句
            cur.execute(open(os.path.join(os.getcwd(),"import.sql"), "r", encoding = 'utf8').read())   
            print(in_table+" is imported!\n")
            
conn.commit()            
cur.close()
conn.close() 