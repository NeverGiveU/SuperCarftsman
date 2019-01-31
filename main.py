# -*- coding:utf-8 -*-


"""

@author: Jan
@file: main.py.py
@time: 2019/1/30 20:40
"""

from flask import Flask, request, render_template, make_response

app = Flask(__name__)

'''home page'''
@app.route('/SuperCraftsman')
def index():
    response = make_response(render_template('index.html'))
    return response
    pass

if __name__ == '__main__':
    app.run(debug=True)