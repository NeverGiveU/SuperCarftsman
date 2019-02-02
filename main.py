# -*- coding:utf-8 -*-


"""

@author: Jan
@file: main.py.py
@time: 2019/1/30 20:40
"""

from flask import Flask, request, render_template, make_response
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

app = Flask(__name__)

'''home page'''
@app.route('/SuperCraftsman')
def index():
    response = make_response(render_template('index.html'))
    return response
    pass

@app.route('/SuperCraftsman/register')
def from_index_to_register():
    response = make_response(render_template('register.html'))
    return response

@app.route('/register', methods=['POST', 'GET'])
def register():
    sig = request.args.get('signal')
    if sig is not None:
        print(sig.signal)
    return 'SUCCESS'


if __name__ == '__main__':
    app.run(debug=True)