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


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #    form.validate_on_submit()等价于request.method==' post '  and  from.validate()-表单里必填项有值
    if form.validate_on_submit():
        # 将提交后的数据显示在页面上
        flash('Login requested for user {},remember_me={}'.format(form.username.data, form.remember_me.data))
        # form.validate_on_submit()=True时，代表登录成功，进入Index页面
        return redirect(url_for('index'))
    # 若未提交数据，则请求后再次转到login页面
    return render_template('login.html', title='Sign In', form=form)
