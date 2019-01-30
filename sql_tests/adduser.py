# -*- coding:utf-8 -*-

"""

@author: Jan
@file: adduser.py
@time: 2019/1/30 16:19
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
for i in range(5):
    sql_manager = "insert into user (account, salt, password, nickname, email) values ('%s', '%s', '%s', '%s', '%s')"%('craftsman', '0000', str(i)*8, 'chopin_fan', "773347598@qq.com")
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql_manager)
        connection.commit()
    except:
        connection.rollback()
    cursor.close()
    print('Successfully create the craftsman {}!'.format(i))