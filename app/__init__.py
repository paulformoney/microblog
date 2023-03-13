from flask import Flask
from config import Config
from flask_login import LoginManager

# 导入SQLAlchemy类，使用其中方法
from flask_sqlalchemy import SQLAlchemy
#
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

# 导入LoginManager类，对app进行处理，返回一个login对象，管理用户登录状态
login = LoginManager(app)

# 设置某些页面必须通过login后才可登录
login.login_view = 'login'


# 数据库对象
db = SQLAlchemy(app)
# 迁移引擎对象
migrate = Migrate(app, db)

from app import routes, models