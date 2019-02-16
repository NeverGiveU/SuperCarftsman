# -*- coding:utf-8 -*-


"""

@author: Jan
@file: main.py.py
@time: 2019/1/30 20:40
"""

from flask import Flask, request, render_template, make_response
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

        outdate = datetime.datetime.today() + datetime.timedelta(days=1)
        ckie = str(uuid.uuid4())

        salt = get_salt()
        sql_manager = "insert into user (account, salt, password, nickname, email, cookie, photopth) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
        account, salt, get_md5(password, salt), nickname, email, ckie, ("../"+'static'+'/'+'src'+'/'+'images'+'/'+'default.png'))
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql_manager)
            connection.commit()
            # print('Successfully create the craftsman {}!'.format(nickname))
            flag = 1
        except:
            connection.rollback()
            flag = -1
        cursor.close()

        count = 0
        sql = "select count(*) as value from user"
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql)
            count = cursor.fetchall()
        except:
            connection.rollback()
        cursor.close()

        # achievement
        sql_manager = "insert into achievement (level, exp, user_id) values (%d, %f, %d)" % (0, 0.0, count[0]['value'])
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql_manager)
            connection.commit()
        except:
            connection.rollback()
        cursor.close()

        response = make_response(simplejson.dumps({
            'res': flag
        }))
        response.set_cookie('cookie', str(uuid.uuid4()), expires=outdate)
        return response

@app.route('/SuperCraftsman/login', methods=['POST', 'GET'])
def login():
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
            # print(data[0])
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

    outdate = datetime.datetime.today() + datetime.timedelta(days=1)
    ckie = str(uuid.uuid4())
    # print(ckie)
    # set cookie
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "update user set cookie='%s' where account='%s'"%(ckie, account)
    response.set_cookie('cookie', ckie, expires=outdate)
    try:
        cursor.execute(sql)
        connection.commit()
        # print("Successful modification!")
    except:
        connection.rollback()
    cursor.close()

    return response

@app.route('/SuperCraftsman/selfinfo', methods=['GET', 'POST'])
def selfinfo():
    response = make_response(render_template('selfinfo.html'))
    return response

"""===================================================================================================== tutorials' part """
@app.route('/SuperCraftsman/tutorialeditor', methods=['GET', 'POST'])
def tutorialeditor():
    response = make_response(render_template('tutorialeditor.html'))
    return response

@app.route('/SuperCraftsman/uploadtutorial', methods=['post'])
def uploadtutorial():
    # print(request.args.get('a'))
    # print("uploadtutorial called")
    title = request.form['tutorial_title']
    classification = request.form['classification']
    title_ = ""

    for i in range(len(title)-1):
        title_ += str(ord(title[i]))
        title_ += '-'
    title_ += str(ord(title[-1]))
    # print(title)
    count = int(request.form['count_val'])
    img_names = []
    txt_names = []
    for i in range(1, count+1):
        img = request.files['imgup_{}'.format(i)]
        img_names.append(img.filename)
        txt = request.form['txtup_{}'.format(i)]
        txt_names.append(txt)
        # print(img.filename)
        # print(txt)
        pass

    # find whether it has been created
    new_flag = False
    state = 1

    # find the user_id according cookie
    ckie = request.cookies.get('cookie')
    if True:
        if ckie is not None:
            # print(ckie)
            # find the usr according to cookie, get the data
            sql = "select * from user where cookie = '%s';" % ckie
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
                if len(data) == 1:
                    state += 1
                    d = data[0]
                    user_id = int(d['id'])
            except:
                connection.rollback()
            cursor.close()

    if state == 2:
        sql = "select * from tutorial where host_id = %d and title = '%s';" % (user_id, title_)
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            print("用中文查询成功")
            print(len(data))
            if len(data) == 0:
                # not found
                state += 1
                # get tutorial count
                count2 = 0
                sql3 = "select count(*) as value from tutorial"
                cursor3 = connection.cursor(cursor=pymysql.cursors.DictCursor)
                try:
                    cursor3.execute(sql3)
                    count2 = (cursor3.fetchall())[0]['value']
                    # print(count)
                except:
                    connection.rollback()
                cursor3.close()

                # newly build dir
                pth = os.path.join(os.getcwd(), 'static', 'tutorials', str(count2+1))
                print(pth)
                if not os.path.exists(pth):
                    # print("dasda")
                    os.mkdir(pth)
                    os.mkdir(os.path.join(pth, 'src'))
                    fobj = open(os.path.join(pth, 'strut.txt'), 'w')
                    fobj.close()
                    fobj = open(os.path.join(pth, 'comment.txt'), 'w')
                    fobj.close()

                # new record
                sql2 = "insert into tutorial (srcpth, title, host_id, classification) values ('%s', '%s', %d, '%s')" % (str(count2+1), title_, user_id, classification)
                cursor2 = connection.cursor(cursor=pymysql.cursors.DictCursor)
                try:
                    cursor2.execute(sql2)
                    connection.commit()
                except:
                    connection.rollback()
                cursor2.close()
            else:
                # the tutorial has already existed
                print("found it!")
                d = data[0]
                pth = d['srcpth']
                pth = os.path.join(os.getcwd(), 'static', 'tutorials', pth)
        except:
            connection.rollback()
        cursor.close()

    # then we try to load the resources
    if state >= 2:
        # we have gotten the pth
        # print(os.listdir(pth))
        images = os.listdir(os.path.join(pth, 'src'))
        for image in images:
            os.remove(os.path.join(pth, 'src', image))
        '''
        for i in range(1, count+1):
            pass
        '''
        # print(img_names)
        # print(txt_names)
        strut = open(os.path.join(pth, 'strut.txt'), 'w', encoding='utf-8')
        strut.write(title + '\n')
        for i in range(1, count + 1):
            img = request.files['imgup_{}'.format(i)]
            img.save(os.path.join(pth, 'src', '{}.png'.format(i)))
            txt = request.form['txtup_{}'.format(i)]
            strut.write(txt + '\n<>\n')
        strut.close()
        pass
    '''
    return simplejson.dumps({
        'state': state
    })
    '''
    if state >= 2:
        return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>新增教程成功！</title>
        <link rel="shortcut icon" href="../static/src/images/logo.ico" type="image/x-icon"/>
    </head>
    <body>
    <p>请关闭此窗口！</p>
    <script type="text/javascript">
        alert("添加教程成功！");
    </script>
    </body>
        """
    else:
        return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>新增教程成功！</title>
                <link rel="shortcut icon" href="../static/src/images/logo.ico" type="image/x-icon"/>
            </head>
            <body>
            <p>请关闭此窗口！</p>
            <script type="text/javascript">
                alert("登录超时导致添加教程失败，请重新登录！");
            </script>
            </body>
                """

@app.route('/SuperCraftsman/gettutorialtxt', methods=['GET', 'POST'])
def gettutorialtxt():
    filename = request.args.get('filename', "")
    filename = filename.split("..")[1].split("/")
    title = ''
    contents = []
    state = 0
    pth = os.path.join(os.getcwd(), filename[1], filename[2], filename[3], filename[4])
    if os.path.exists(pth):
        state = 1
        fhandle = open(pth, 'r', encoding='UTF-8')
        line = fhandle.readline()
        title = line
        line = fhandle.readline()
        contents = []
        content = []
        while line:
            if line == '<>\n':
                if content != []:
                    contents.append(content)
                    content = []
                pass
            else:
                if line != '\n':
                    content.append(line)

            line = fhandle.readline()
        fhandle.close()
        # print(contents)
    return simplejson.dumps({
        'state': state,
        'title': title,
        'content': contents
    })

@app.route('/SuperCraftsman/tutorialdetails', methods=['GET', 'POST'])
def tutorialdetails():
    response = make_response(render_template('tutorialdetails.html'))
    return response

@app.route('/SuperCraftsman/gettutorials', methods=['GET', 'POST'])
def gettutorials():
    state = request.args.get('state', 0)
    sql = "select * from tutorial"
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)

    tut_ids = []
    host_ids = []
    host_names = []
    host_photos = []
    titles = []
    if int(state) == 1:
        type = request.args.get('type', '')
        print(type)
        pass
    else:
        print(state)
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            # print(data)
            if len(data) > 0:
                if int(state) == -2:
                    r = min(4, len(data))
                    # print(r)
                if int(state) == -1:
                    r = len(data)
                    # print(r)
                state = 2
                # get at most 4
                data.reverse()
                for i in range(r):
                    d = data[i]
                    tut_ids.append(d['id'])
                    host_ids.append(d['host_id'])
                    titles.append(d['title'])
                pass
        except:
            print('fail1')
            connection.rollback()
        cursor.close()



    # decode the titles
    for i in range(len(titles)):
        title = titles[i]
        title = title.split("-")
        for j in range(len(title)):
            title[j] = chr(int(title[j]))
        titles[i] = ''.join(title)
    # print(titles)
    #print(host_ids)
    if state == 2:
        for host_id in host_ids:
            sql = "select * from user where id = %d"%(host_id)
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
                if len(data) > 0:
                    host_names.append(data[0]['nickname'])
                    host_photos.append(data[0]['photopth'])
            except:
                print('fail2')
                connection.rollback()
            cursor.close()
    #print(host_photos)
    return simplejson.dumps({
        'state': state,
        'tut_ids': tut_ids,
        'host_ids': host_ids,
        'host_names': host_names,
        'host_photos': host_photos,
        'titles': titles
    })

@app.route('/SuperCraftsman/tutorials-ocean', methods=['GET', 'POST'])
def tutorialsocean():
    response = make_response(render_template('tutorials-ocean.html'))
    return response

"""===================================================================================================== users' part """
@app.route('/SuperCraftsman/validation', methods=['GET', 'POST'])
def validation():
    # print("Validation Called")            # -1        none
    state = int(request.args.get('state', 0))
    ckie = request.cookies.get('cookie')
    nickname = None
    account = None
    email = None
    sex = None
    birth = None
    province = None
    city = None
    county = None
    procession = None
    signature = None
    photopth = None
    user_id = None
    if state == -1:
        # asking for request
        state += 1                          # 0         get dealt
        if ckie is not None:
            # print(ckie)
            # user information
            sql = "select * from user where cookie = '%s';" % ckie
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
            state += 1                      # 1         with cookie
            nickname = None
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
                if len(data) > 0:
                    state += 1              # 2         validated
                    # print(data[0])
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
                        user_id  =d['id']
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

            sel_year, sel_month, sel_day = -1, -1, -1
            if birth is not None:
                birth = str(birth)
                sel_year = int(birth.split('-')[0])
                sel_month = int(birth.split('-')[1])
                sel_day = int(birth.split('-')[-1])
            # get tutorial paths
            t_pths = []
            if state == 2:
                sql = "select * from tutorial where host_id = %d;" % (user_id)
                cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
                try:
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    for d in data:
                        t_pths.append(d['id'])
                except:
                    pass
                cursor.close()
                print(t_pths)

            return simplejson.dumps({
                'state': state,
                'nickname': nickname,
                'account': account,
                'email': email,
                'sex': sex,
                'sel_year': sel_year,
                'sel_month': sel_month,
                'sel_day': sel_day,
                'province': province,
                'city': city,
                'county': county,
                'procession': procession,
                'signature': signature,
                'photopth': photopth,
                't_pths': t_pths,
                'user_id': user_id
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
    img, nickname, email, procession, signature, sel_year, sel_month, sel_day, province, city, area = \
        None, None, None, None, None, None, None, None, None, None, None
    whether_to_modify_the_photo = False

    try:
        img = request.files['head_img']
        whether_to_modify_the_photo = True
    except:
        pass
    try:
        nickname = request.form['nickname']
        email = request.form['email']
        procession = request.form['procession']
        signature = request.form['signature']
        sex = request.form['sex']
        sel_year = int(request.form['sel_year'])
        sel_month = int(request.form['sel_month'])
        sel_day = int(request.form['sel_day'])
        province = request.form['province']
        city = request.form['city']
        area = request.form['area']
    except:
        pass

    '''
    if (nickname is not None) and (email is not None) and (procession is not None) and (signature is not None) and\
            (sel_year is not None) and (sel_month is not None) and (sel_day is not None) and \
            (province is not None) and (city is not None) and (area is not None):
    '''

    print(nickname)
    print(email)
    print(procession)
    print(signature)
    print(sel_year)
    print(sel_month)
    print(sel_day)
    print(province)
    print(city)
    print(area)
    print(sex)

    state = 0
    time_ = str(int(time.time()))
    # print(img.filename)
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
                print(data[0])
                for d in data:
                    account = d['account']

                    # clean all the past images
                    if whether_to_modify_the_photo is True:
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
    # print(state)

    if state == 2:
        # then we want to find update the info
        pth = "../" + 'static/resources' + '/' + account + '/' + '{}_head.png'.format(time_)
        # print(pth)
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        birthday = "{}-{}-{}".format(sel_year, sel_month, sel_day)
        if whether_to_modify_the_photo is True:
            sql = "update user set photopth='%s', nickname='%s', email='%s', sex='%s', procession='%s', signature='%s', " \
                  "province='%s', ciy='%s', county='%s', birth='%s' where account='%s'" % \
                  (pth, nickname, email, sex, procession, signature, province, city, area, birthday, account)
            # print("{}-{}".format(whether_to_modify_the_photo, 1))
        else:
            sql = "update user set nickname='%s', email='%s', sex='%s', procession='%s', signature='%s', " \
                  "province='%s', ciy='%s', county='%s', birth='%s' where account='%s'" % \
                  (nickname, email, sex, procession, signature, province, city, area, birthday, account)
            # print("{}-{}".format(whether_to_modify_the_photo, 2))
        try:
            cursor.execute(sql)
            connection.commit()
            # print("Successful modification!")
        except:
            connection.rollback()
            # print("Failed modification!")
        cursor.close()


    response = make_response(render_template('selfinfo.html'))
    return response

# 个人主页
@app.route('/SuperCraftsman/selfhome')
def selfhome():
    response = make_response(render_template('selfhome.html'))
    return response

"""=================================================================================================== comment' part """
"""
sql_cmm = '''create table comment(
id int primary key auto_increment,
gdatetime datetime,
context text(1000),
usr_id int,
num_like int,
tutorial_id int,
foreign key(tutorial_id) references tutorial(id),
reply_id int default -1
)'''
"""
@app.route('/SuperCraftsman/uploadcomment', methods=['post'])
def uploadcomment():
    # get user_id
    ckie = request.cookies.get('cookie')
    sql = "select * from user where cookie = '%s';" % ckie
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
    state = -1
    user_id = -1
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) > 0:
            state += 1
            for d in data:
                user_id = d['id']
    except:
        connection.rollback()
    cursor.close()
    print(user_id)

    flag = False
    try:
        txt_comment = request.form['my_txt_comment']
        tut_id = request.form['save_id']
        flag = True
    except:
        pass

    if flag:
        sql_comment = "insert into comment (context, usr_id, num_like, tutorial_id, reply_id) values ('%s', %d, %d,%d, -1)" % (txt_comment, int(user_id), 0, int(tut_id))
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql_comment)
            connection.commit()
            print('Successfully create the comment!')
            flag = 1
        except:
            connection.rollback()
            flag = -1
        cursor.close()

        print(txt_comment)
        pass
    return 'success'

@app.route('/SuperCraftsman/addcomment', methods=['GET'])
def addcomment():
    state = -1
    cmm_id = request.args.get('id', 0)
    print(cmm_id)
    sql = "select * from comment where tutorial_id = %d and reply_id = %d;" % (int(cmm_id), -1)
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
    state += 1
    usr_ids = []
    usr_accounts = []
    usr_photopths = []
    cmm_ids = []
    comments = []
    date_stamps = []

    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) > 0:
            state = 1
            for d in data:
                usr_ids.append(d['usr_id'])
                cmm_ids.append(d['id'])
                comments.append(d['context'])
                date_stamps.append(str(d['gdatetime']))
            pass
    except:
        connection.rollback()

    for usr_id in usr_ids:
        usr_account = ''
        usr_photopth = ''
        sql = "select * from user where id = %d;" % int(usr_id)
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) > 0:
                usr_account = data[0]['account']
                usr_photopth = data[0]['photopth']
                pass
        except:
            connection.rollback()
        usr_accounts.append(usr_account)
        usr_photopths.append(usr_photopth)
        pass
    print(usr_photopths)
    return simplejson.dumps({
        'state': state,

        'usr_ids': usr_ids,
        'usr_acounts': usr_accounts,
        'usr_photopths': usr_photopths,
        'cmm_ids': cmm_ids,
        'comments': comments,
        'date_stamps': date_stamps
    })

@app.route('/SuperCraftsman/uploadreply', methods=['post'])
def uploadreply():
    txt_reply = ''
    to_id = 0
    from_id = 0
    usr_id = 0
    try:
        txt_reply = request.form['txt_reply']
        hidden_info = request.form['hidden_info']
        try:
            to_id = int(hidden_info.split('-')[1])  # reply to which comment
            from_id = int(hidden_info.split('-')[3])# for which tutorial
            usr_id = int(hidden_info.split('-')[2]) # from which user
        except:
            pass
    except:
        pass
    # print(txt_reply)
    # print(hidden_info)
    if from_id == 0:
        print("nothing to do")
    else:
        sql_comment = "insert into comment (context, usr_id, num_like, tutorial_id, reply_id) values ('%s', %d, %d,%d, %d)" % (txt_reply, usr_id, 0, from_id, to_id)
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql_comment)
            connection.commit()
            # print('Successfully create the comment!')
        except Exception as e:
            # print(e)
            connection.rollback()
        cursor.close()

        pass
    return 'success'

@app.route('/SuperCraftsman/getreply', methods=['GET',' POST'])
def getreply():
    reply_to_id = request.args.get('reply_id', 0)
    print(reply_to_id)
    state = -1
    sql = "select * from comment where reply_id = %d;" % (int(reply_to_id))
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)

    usr_ids = []
    usr_accounts = []
    usr_photopths = []
    cmm_ids = []
    replies = []
    date_stamps = []

    try:
        cursor.execute(sql)
        data = cursor.fetchall()

        for d in data:
            # print(d)
            usr_ids.append(d['usr_id'])
            replies.append(d['context'])
            date_stamps.append(str(d['gdatetime']))
            state = 1
    except:
        connection.rollback()
    if state == 1:
        for usr_id in usr_ids:
            sql = "select * from user where id = %d"%(usr_id)
            cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
                usr_photopths.append(data[0]['photopth'])
            except:
                connection.rollback()
    print(replies)
    print(date_stamps)
    return simplejson.dumps({
        'state': state,
        'no': 'no',
        'usr_ids': usr_ids,
        'replies': replies,
        'date_stamps': date_stamps,
        'usr_photopths': usr_photopths
    })

if __name__ == '__main__':
    app.run(debug=True)
