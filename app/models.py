from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# 关系表，无需定义类，由类表连接生成
follwers = db.Table(
    # 关系表名
    "follower",
    # 第一个参数，粉丝id，外键为user.id
    db.Column('follwer_id', db.Integer, db.ForeignKey('user.id')),

    # 第二个参数，被关注者id，外键为user.id
    db.Column('follwed_id', db.Integer, db.ForeignKey('user.id')),

)


# 多继承，通过继承UserMixin实现登录属性is_auth（已登录True，未登录False）
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    about_me = db.Column(db.String(140))
    last_seen_time = db.Column(db.DateTime, default=datetime.utcnow)

    # followed表示被xx关注，使用User().followed可获取当前用户的所有粉丝
    followed = db.relationship(
        # User自身产生的followed关系
        'User',

        # 记录该关系名称的表，即上面定义的follwers表
        secondary=follwers,

        # 粉丝id，指定了左侧实体（关注者）与关联表链接的条件
        primaryjoin=(follwers.c.follwer_id == id),

        # 被关注者id，指定了右侧实体（被关注者）与关联表链接的条件
        secondaryjoin=(follwers.c.follwed_id == id),

        # 关系，从右侧查询时，关系名为followers，即User().followers可获取你关注了xx
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )


    # backref='author'，新增一条Post数据时，author为参数名，值为一条user对象
    # User().posts，获取user在post表中所有关联数据
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 判断用户是否已被关注，即筛选当前对象是否在关系表中有记录（当前用户为followed），若大于0（代表有被关注）则返回True，否则返回False
    def is_following(self, user):
        return self.followed.filter(follwers.c.follwed_id == user.id).count() > 0

    # 关注一个用户，即增加一条记录：followed_id=user.id，follower_id=self.id→self.followed.append(user)
    def follow(self, user):
        # 先判断self和user的关系，若未关注，则新增关注关系
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)


    def followed_posts(self):
        followed = Post.query.join(follwers,
                                   (follwers.c.follwed_id == Post.user_id)).\
            filter(follwers.c.follwer_id==self.id).order_by(Post.timestamp.desc())
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User {}, Email {}, Password_Hash {}, Posts {}'.format(self.username, self.email, self.password_hash,
                                                                       self.posts)
    # User类的新方法avatar()返回用户头像的URL，并缩放到请求的大小（以像素为单位）
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}'.format(self.body)


# 用户加载函数，用于调用加载指定ID的用户
# ID是Flask-login在用户会话中存储的唯一标识符，用于标记用户，用户通过其
# 连接到自己的存储空间，如登录后，跳转到个人资料页，要显示指定用户的资料
# 此时区分用户的方法就是ID，由于Flask-login无法直接获取数据库id，所以通过
# 此方法获取指定ID对应的用户
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
