from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    user = {"username":"paul"}
    # 列表存储两个字典，代表两个用户与其发布的微博
    posts = [
        {'author':{'username':'uzi'},
         'body':'薇恩'
         },
        {
            'author':{'username':'rookie'},
            'body':'发条'
        }
    ]
    return render_template('index.html', title='Home', user=user,posts=posts)


@app.route('/user/<name>')
def user(name):
    return f"hello,{name}"
# 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