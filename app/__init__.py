import logging

from flask import Flask
from config import Config
from flask_login import LoginManager

# 导入SQLAlchemy类，使用其中方法
from flask_sqlalchemy import SQLAlchemy
# 数据库迁移类，用于保存原有数据的情况下升级数据库（如新增字段，新增表）
from flask_migrate import Migrate


# 日志类，记录接口报错并写入日志问价
from logging.handlers import RotatingFileHandler
import os



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

if not app.debug:
    # 若不存在logs文件夹，则在当前目录下创建
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # 实例化一个日志写入对象，规定名称为microblog.log，位置为/orange/microblog/logs/，backupCount=10代表日志文件最大数量为10个，超过10个删除最老的
    # maxBytes=10240代表该日志文件最大为10240个字节数，超过则分割到下一个文件中
    file_handler = RotatingFileHandler('/orange/microblog/logs/microblog.log', maxBytes=10240, backupCount=10)
    # 格式化写入时间、等级、日志内容、报错代码路径
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    # 设置
    file_handler.setLevel(logging.INFO)
    # 设置完成日志的格式后，将其添加给app(即博客项目app)，即可收集app执行过程中控制台的输出兵写入日志
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')



from app import routes, models, errors