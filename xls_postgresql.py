'''
Created 
xls文件导入postgresql数据库
@author: hwt
'''

import xlrd, psycopg2,sys
reload(sys)
sys.setdefaultencoding('utf8')
conn = psycopg2.connect(database="maqin",user="postgres",password="fendou2015",host="localhost",port=5432)
cur = conn.cursor()
cur.execute("SET CLIENT_ENCODING TO 'utf8';")
cur.execute("SET search_path TO maqin_test")
#execSql = "CREATE TABLE maqin_ghq_spatial_2016 (gh_id varchar,lin_ban varchar,xiao_ban varchar,xxb varchar,mian_ji numeric);"
#cur.execute(execSql)
# execSql1 = "CREATE TABLE maqin_ghq_hly_2016 (gh_id varchar, xingming varchar, xzc varchar,cun_hly varchar shenfen_id varchar);"
# cur.execute(execSql1)
# conn.commit()
data = xlrd.open_workbook('d:/maqin_menyuan_data/tianbaoguanhuqujijingzhunfupinhulinyuan2016.xls')
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
tag = ''
for i in range(nrows):
    if i > 0:
        rowData = table.row_values(i)
        mianji = round(rowData[8]/15,1)
        if rowData[41] != '':
            rowData[41] = str(rowData[41])[0]
            first = "INSERT INTO maqin_ghq_spatial_2016 (mian_ji,gh_id,lin_ban,xiao_ban,xxb,xiang) " \
                "VALUES (%s,'%s','%s','%s','%s'" % (mianji, str(rowData[0]), rowData[5], rowData[6], rowData[41])
        else:
		    first = "INSERT INTO maqin_ghq_spatial_2016 (mian_ji,gh_id,lin_ban,xiao_ban,xiang) " \
                "VALUES (%s,'%s','%s','%s'" % (mianji, str(rowData[0]), rowData[5], rowData[6])
        if rowData[43] == '':
            rowData[43] = 'null'
        if rowData[44] == '':
            rowData[44] = 'null'
        # first = "INSERT INTO maqin_ghq_spatial_2016 (mian_ji,gh_id,lin_ban,xiao_ban,xxb,xiang) " \
        #          "VALUES (%s,'%s','%s','%s','%s'" % (mianji, str(rowData[0]), rowData[5], rowData[6], rowData[41])
        second = ",'" + rowData[1] + "');"
        print first+second
        # execSql = "INSERT INTO maqin_ghq_spatial_2016 (mian_ji,gh_id,xiang,lin_ban,xiao_ban,xxb) " \
        #           "VALUES (%s"% mianji+",'"+rowData[0] + "','" + rowData[1] + "','" + rowData[5]+"','"+rowData[6]+"','"+rowData[41] + "');"
        # execSql = "INSERT INTO maqin_ghq_spatial_2016 (gh_id,xiang,lin_ban,xiao_ban,xxb,mian_ji) VALUES (%s,%s,%s,%s,%s,%s)" \
        #           % (rowData[0],rowData[1],rowData[5],rowData[6],rowData[41],mianji)
        cur.execute(
            first+second
        )
        # if rowData[0] != tag:
        #     tag = rowData[0]
        #     cur.execute(
        #         "INSERT INTO maqin_ghq_hly_2016 (gh_id,xingming,xiang,cun_hly,shenfen_id,beizhu) "+
        #         "VALUES ('"+str(rowData[0]) + "','" + rowData[3]+"','"+rowData[1]+"','"+rowData[2]+"','"+rowData[4]+"','" + rowData[44]+"');"
        #     )
conn.commit()
cur.close()
conn.close()
