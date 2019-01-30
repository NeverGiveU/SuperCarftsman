# -*- coding:utf-8 -*-


"""

@author: Jan
@file: saltHashing.py.py
@time: 2019/1/30 13:35
"""

from random import Random
from hashlib import md5


'''randomly get a 4-byte salt'''
def get_salt(length=4):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    range_chars = len(chars) - 1
    random_obj = Random()

    for i in range(length):
        salt = salt + chars[random_obj.randint(0, range_chars)]
    # print(salt)
    return salt

'''compute the hashing'''
def get_md5(pwd, salt):
    md5_obj = md5()
    md5_obj.update((pwd + salt).encode("utf8"))
    return md5_obj.hexdigest()

'''example'''
'''
pwd = '20190130'
salt = get_salt()
md5_val = get_md5(pwd=pwd, salt=salt)
print(md5_val)
print(len(md5_val))
'''