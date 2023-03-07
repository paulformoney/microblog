import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'

    # 从环境变量中获取数据库信息，若没有该数据库则会创建一个名为app.db的数据库，存在basedir中
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # 不需要了解
    SQLALCHEMY_TRACK_MODIFICATIONS = False