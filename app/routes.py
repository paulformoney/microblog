from app import app, db
from flask import request, render_template, flash, redirect, url_for
from app.form import LoginForm, RegisterForm
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User
from werkzeug.urls import url_parse


# login_required，添加了该修饰器的页面必须为登录状态才可访问
@app.route('/')
@app.route('/index')
@login_required
def index():
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
    return render_template('index.html', title='Home', posts=posts)


@app.route('/user/<name>')
def user(name):
    return f"hello,{name}"
# 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


@app.route('/login', methods=['GET', 'POST'])
def login():

    # current_user，当前会话，is_authenticated,属性，已登录-True,未登录-False
    # 若用户已登录，进入login页后直接跳转到个人主页，若未登录则去登录页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    #    form.validate_on_submit()等价于request.method==' post '  and  from.validate()-表单里必填项有值
    if form.validate_on_submit():

        # 根据表单输入的用户名去数据表中查询用户
        user = User.query.filter_by(username=form.username.data).first()

        # 若用户不存在或用户存在但表单密码未通过则报错，提示错误信息并重定向到登录页，若通过该if则登录成功进入index页
        if user is None or user.check_password(password=form.password.data)==False:
            flash('Username or Password Invalid')
            return redirect(url_for('login'))

        # 将提交后的数据显示在页面上
        flash('Login requested for user {},remember_me={}'.format(form.username.data, form.remember_me.data))

        login_user(user, remember=form.remember_me.data)


        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # 若未提交数据，则请求后再次转到login页面
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    # 从app引入db,app.models引入User，获取前端提交表单中的数据，作为参数实例化一个user对象并提交
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html',title="Sign In",form=form)
