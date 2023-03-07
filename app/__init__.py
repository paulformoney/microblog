from flask import Flask
from config import Config

# 导入SQLAlchemy类，使用其中方法
from flask_sqlalchemy import SQLAlchemy
#
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

# 数据库对象
db = SQLAlchemy(app)
# 迁移引擎对象
migrate = Migrate(app, db)

from app import routes, models