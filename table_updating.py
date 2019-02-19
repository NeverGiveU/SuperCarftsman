# -*- coding:utf-8 -*-


"""

@author: Jan
@file: table_updating.py
@time: 2019/2/18 19:22
"""
import pymysql

# connect to the database
connection = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user='root',
    password='Winer20Chopin@',# modify the password here
    charset='utf8',
    database="craftsman"
)

sql = "alter table user add column grades int default 100 not null;"
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql)
cursor.close()

sql = "alter table user modify column grades float ;"
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql)
cursor.close()

sql = "alter table likes change tut_like tut_id int;"
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql)
cursor.close()

sql_cmm = '''create table likes(
id int primary key auto_increment,
usr_id int default 0,
tut_id int default 0
)'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_cmm)
cursor.close()
print('Successfully create table \'likes\'!')