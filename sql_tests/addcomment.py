# -*- coding:utf-8 -*-


"""

@author: Jan
@file: addcomment.py
@time: 2019/1/30 16:38
"""

import pymysql

# connect to the database
connection = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user='root',
    password='Winer20Chopin@',
    charset='utf8',
    database="craftsman"
)
for i in range(3):
    sql_manager = "insert into comment (context) values ('%s')"%('helloworld {}!'.format(i))
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql_manager)
        connection.commit()
    except:
        connection.rollback()
    cursor.close()
    print('Successfully create the comment {}!'.format(i))