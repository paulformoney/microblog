from app import app, db
from flask import request, render_template, flash, redirect, url_for
from app.form import LoginForm, RegisterForm, EditProfileForm
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, follwers
from werkzeug.urls import url_parse
from datetime import datetime


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


@app.route('/user/<username>')
@login_required
def user(username):
    # first_or_404，若未找到结果返回404错误
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


# 新增函数，记录发起请求的时间，由于current_user的机制，无需db.commit.add()
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# 新增路由，处理提交编辑个人资料的表单内容并提交到数据库，必须为登录状态才可使用
@app.route('/user/profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    # 若为post请求（用户提交了个人资料数据），则将表单中的数据赋给当前用户并commit
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        # current_user机制下，commit即视为commit+add
        db.session.commit()
        flash('Your changes have been saved.')
        # 返回页面
        return redirect(url_for('edit_profile'))

    # 若方法为get，则将当前用户的数据返回给表单并显示
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>')
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not fount'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('you cannot follow yourself')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('you are following {}'.format(username))
    return redirect(url_for('user', username=username))