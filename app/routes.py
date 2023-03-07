from app import app
from flask import render_template, flash, redirect, url_for
from app.form import LoginForm


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


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    # validate_on_submit():form表单请求为get方法时返回False,Post方法返回True
    if form.validate_on_submit():
        flash('Login request for user {},remember me={}'.format(form.username.data,form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign in',form=form)