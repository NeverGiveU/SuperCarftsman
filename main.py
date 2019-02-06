# -*- coding:utf-8 -*-


"""

@author: Jan
@file: main.py.py
@time: 2019/1/30 20:40
"""

from flask import Flask, request, render_template, make_response, redirect, url_for
import pymysql
import simplejson
import uuid
import os
from saltHashing import get_md5, get_salt
import datetime
from PIL import Image
import time

# connect to the database
connection = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user='root',
    password='Winer20Chopin@',
    charset='utf8',
    database="craftsman"
)

'''
-1 -- failure
+1 -- success
+2 -- repeated
'''

app = Flask(__name__)

'''home page'''
@app.route('/SuperCraftsman')
@app.route('/index')
def index():
    response = make_response(render_template('index.html'))
    ckie = request.cookies.get('cookie')
    if ckie is None:
        outdate = datetime.datetime.today() + datetime.timedelta(days=1/24)
        response.set_cookie('cookie', str(uuid.uuid4()), expires=outdate)
    # print(ckie)
    return response

@app.route('/SuperCraftsman/register')
def from_index_to_register():
    nickname = request.args.get('nickname', '')
    account = request.args.get('account', '')
    email = request.args.get('email', '')
    password = request.args.get('password', '')
    password2 = request.args.get('password2', '')
    if nickname == '' and account == '' and email == '' and password == '' and password2 == '':
        response = make_response(render_template('register.html'))
        return response
    else:
        flag = 0
        '''make sure not repeated accounts'''
        sql = "select * from user where account = '%s';" % account
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        # nickname = None
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) > 0:
                flag = 2
                return simplejson.dumps({
                    'res': flag
                })
        except:
            connection.rollback()
        cursor.close()

        '''add new account'''
        path = os.path.join(os.getcwd(), 'static', 'resources', account)
        if not os.path.exists(path):
            os.mkdir(path)

        outdate = datetime.datetime.today() + datetime.timedelta(days=1 / 24)
        ckie = str(uuid.uuid4())

        salt = get_salt()
        sql_manager = "insert into user (account, salt, password, nickname, email, cookie, photopth) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
        account, salt, get_md5(password, salt), nickname, email, ckie, ("../"+'static'+'/'+'src'+'/'+'images'+'/'+'default.png'))
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql_manager)
            connection.commit()
            print('Successfully create the craftsman {}!'.format(nickname))
            flag = 1
        except:
            connection.rollback()
            flag = -1
        cursor.close()

        response = make_response(simplejson.dumps({
            'res': flag
        }))
        response.set_cookie('cookie', str(uuid.uuid4()), expires=outdate)
        return response

@app.route('/SuperCraftsman/login', methods=['POST', 'GET'])
def login():
    # print(ckie)

    # print('2123')
    account = request.args.get('account', '')
    password = request.args.get('password', '')

    sql = "select * from user where account = '%s';" % account
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
    state = -1
    nickname = None
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) > 0:
            print(data[0])
            for d in data:
                salt = d['salt']
                pwdh = d['password']
                pwdh_ = get_md5(password, salt)
                # print("{} -- {}".format(pwdh, pwdh_))
                if pwdh_ == pwdh:
                    state = 1
                    nickname = d['nickname']
                    break
    except:
        connection.rollback()
    cursor.close()

    response = make_response(simplejson.dumps({
        'state': state,
        'nickname': nickname
    }))

    outdate = datetime.datetime.today() + datetime.timedelta(days=1 / 24)
    ckie = str(uuid.uuid4())
    print(ckie)
    # set cookie
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "update user set cookie='%s' where account='%s'"%(ckie, account)
    response.set_cookie('cookie', ckie, expires=outdate)
    try:
        cursor.execute(sql)
        connection.commit()
        print("Successful modification!")
    except:
        connection.rollback()
    cursor.close()

    return response

@app.route('/SuperCraftsman/selfinfo', methods=['GET', 'POST'])
def selfinfo():
    response = make_response(render_template('selfinfo.html'))
    return response

"""===================================================================================================== users' part """
@app.route('/SuperCraftsman/validation', methods=['GET', 'POST'])
def validation():
    # print("Validation Called")            # -1        none
    state = int(request.args.get('state', 0))
    ckie = request.cookies.get('cookie')
    if state == -1:
        # asking for request
        state += 1                          # 0         get dealt
        if ckie is not None:
            print(ckie)
            # find the usr according to cookie, get the data
            sql = "select * from user where cookie = '%s';" % ckie
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
            state += 1                      # 1         with cookie
            nickname = None
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
                if len(data) > 0:
                    state += 1              # 2         validated
                    print(data[0])
                    for d in data:
                        nickname = d['nickname']
                        account  =d['account']
                        email = d['email']
                        sex = d['sex']
                        birth = d['birth']
                        province = d['province']
                        city = d['ciy']
                        county = d['county']
                        procession = d['procession']
                        signature = d['signature']
                        photopth =d['photopth']
                        '''
                        print(nickname)
                        print(account)
                        print(email)
                        print(sex)
                        print(birth)
                        print(province)
                        print(city)
                        print(county)
                        print(procession)
                        print(signature)
                        print(photopth)
                        '''
            except:
                connection.rollback()
            cursor.close()
            # print("dadsda1")
            return simplejson.dumps({
                'state': state,
                'nickname': nickname,
                'account': account,
                'email': email,
                'sex': sex,
                'birth': birth,
                'province': province,
                'city': city,
                'county': county,
                'procession': procession,
                'signature': signature,
                'photopth': photopth
            })
        pass
    return 'SUCCESS'

@app.route('/SuperCraftsman/infoeditor')
def infoeditor():
    response = make_response(render_template('infoeditor.html'))
    return response

# 上传图片（头像）
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPEG'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/SuperCraftsman/uploadinfo', methods=['post'])
def uploadinfo():
    # print("Upload is called")
    state = 0
    img = request.files['head_img']
    time_ = str(int(time.time()))
    # print(img.filename)
    if allowed_file(img.filename):
        # img.save('temp.png')
        # get the account
        ckie = request.cookies.get('cookie')
        # asking for request
        if ckie is not None:
            print(ckie)
            state += 1
            # find the usr according to cookie, get the data
            sql = "select * from user where cookie = '%s';" % ckie
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
                if len(data) > 0:
                    state += 1
                    # print(data[0])
                    for d in data:
                        nickname = d['nickname']
                        account = d['account']
                        email = d['email']
                        sex = d['sex']
                        birth = d['birth']
                        province = d['province']
                        city = d['ciy']
                        county = d['county']
                        procession = d['procession']
                        signature = d['signature']
                        photopth = d['photopth']

                        # clean all the past images
                        pth = os.path.join(os.getcwd(), 'static', 'resources', account)
                        ls = os.listdir(pth)
                        for i in ls:
                            c_path = os.path.join(pth, i)
                            os.remove(c_path)

                        # to update the images
                        pth = os.path.join(os.getcwd(), 'static', 'resources', account, '{}_head.png'.format(time_))
                        img.save(pth)
                        # read out and reshape
                        width = img.size[0]
                        height = img.size[1]
                        ratio = 200 / min(width, height)
                        width = ratio * width
                        height = ratio * height
                        img = Image.open(pth).convert('RGB')
                        img = img.resize((width, height), Image.ANTIALIAS)
                        img.save(pth)

            except:
                connection.rollback()
            cursor.close()
        # save the img
        pass
    if state == 2:
        # then we want to find update the info
        pth = "../" + 'static/resources' + '/' + account + '/' + '{}_head.png'.format(time_)
        print(pth)
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "update user set photopth='%s' where account='%s'" % (pth, account)
        try:
            cursor.execute(sql)
            connection.commit()
            print("Successful modification!")
        except:
            connection.rollback()
        cursor.close()

    response = make_response(render_template('infoeditor.html'))
    return response

if __name__ == '__main__':
    app.run(debug=True)