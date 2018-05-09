'''
Created on 2018年5月4日
处理字段对应属性域表field_domain
@author: piaopiao
'''
import psycopg2
import os
from pinyinutil import *

#连接数据库
conn = psycopg2.connect(database="liaoning",user="postgres",password="472594-piao",host="localhost",port=5432)
cur = conn.cursor()
cur.execute("SET CLIENT_ENCODING TO 'utf8';")

query = "select * from public.field_domain where domain_name!=''"
#执行sql语句
cur.execute(query)   
results = cur.fetchall()
for row in results:
    domain_update_sql = "update public.field_domain "\
    "set domain_name = '%s' where domain_name = '%s'" %(to_pinyin(str(row[2])), str(row[2]))
    print(domain_update_sql) 
    cur.execute(domain_update_sql)    
          
conn.commit()            
cur.close()
conn.close() 