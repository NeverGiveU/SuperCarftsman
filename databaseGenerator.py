# -*- coding:utf-8 -*-


"""

@author: Jan
@file: databaseGenerator.py.py
@time: 2019/1/30 13:11
"""
import pymysql
from saltHashing import get_md5

# connect to the database
connection = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user='root',
    password='Winer20Chopin@',
    charset='utf8',
    database="craftsman"
)

'''drop all the tables'''
sql_del = '''drop table if exists collection'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_del)
cursor.close()
print('Successfully delete table \'collection\'!')

sql_del = '''drop table if exists focus'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_del)
cursor.close()
print('Successfully delete table \'focus\'!')

sql_del = '''drop table if exists fan'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_del)
cursor.close()
print('Successfully delete table \'fan\'!')

sql_del = '''drop table if exists comment'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_del)
cursor.close()
print('Successfully delete table \'comment\'!')

sql_del = '''drop table if exists tutorial'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_del)
cursor.close()
print('Successfully delete table \'tutorial\'!')

sql_del = '''drop table if exists achievement'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_del)
cursor.close()
print('Successfully delete table \'achievement\'!')

sql_del = '''drop table if exists user'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_del)
cursor.close()
print('Successfully delete table \'user\'!')


'''------------------------------------------------------------------------------------------------create table: USER'''
sql_usr = """create table user(
id int primary key auto_increment,
account char(30) not null,
salt char(5) not null,
password char(40) not null,
nickname char(20) not null, 
email char (60) not null,
sex enum('male', 'female') default 'male',
birth date,
province char(20), ciy char(20), county char(20),
procession char(20),
signature text(200),
photopth char (50)
)"""
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_usr)
cursor.close()
print('Successfully create table \'user\'!')

'''-----------------------------------------------------------------------------------------create table: ACHIEVEMENT'''
sql_ach = '''create table achievement(
id int primary key auto_increment,
level int,
exp double,
user_id int unique,
foreign key(user_id) references user(id)
on update cascade 
on delete cascade 
)'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_ach)
cursor.close()
print('Successfully create table \'achievement\'!')

'''------------------------------------------------------------------------------------------------create table: FANS'''
sql_fan = '''create table fan(
id int primary key auto_increment,
slave_id int,
host_id int,
foreign key(host_id) references achievement(id)
)'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_fan)
cursor.close()
print('Successfully create table \'fan\'!')

'''-----------------------------------------------------------------------------------------------create table: FOCUS'''
sql_fan = '''create table focus(
id int primary key auto_increment,
hero_id int,
nulike int,
host_id int,
foreign key(host_id) references achievement(id)
)'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_fan)
cursor.close()
print('Successfully create table \'focus\'!')

'''------------------------------------------------------------------------------------------create table: collection'''
sql_col = '''create table collection(
id int primary key auto_increment,
host_id int,
foreign key(host_id) references achievement(id),
tutorial_id int
)
'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_col)
cursor.close()
print("Successfully create table \'collection\'!")

'''--------------------------------------------------------------------------------------------create table: tutorial'''
sql_tut = '''create table tutorial(
id int primary key auto_increment,
srcpth char(100),
host_id int,
foreign  key(host_id) references achievement(id)
)
'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_tut)
cursor.close()
print('Successfully create table \'comment\'!')

'''---------------------------------------------------------------------------------------------create table: COMMENT'''
sql_cmm = '''create table comment(
id int primary key auto_increment,
gdatetime datetime,
context text(1000),
usr_id int,
numlike int,
tutorial_id int,
foreign key(tutorial_id) references tutorial(id),
reply_id int default -1
)'''
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute(sql_cmm)
cursor.close()
print('Successfully create table \'comment\'!')

'''------------------------------------------------------------------------------------------------create the manager'''
sql_manager = "insert into user (account, salt, password, nickname, email) values ('%s', '%s', '%s', '%s', '%s')"%('manager', '0000', get_md5('752025', '0000'), 'chopin', "773347598@qq.com")
cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
try:
    cursor.execute(sql_manager)
    connection.commit()
except:
    connection.rollback()
cursor.close()
print('Successfully create the manager \'user\'!')

connection.close()
