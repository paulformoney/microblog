from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired


# 登录表单，继承FlaskForm
class LoginForm(FlaskForm):
    # 第一个属性username，表单数据类型为StringField，第一个参数即页面显示参数名
    # 第二个参数validators=[DataRequired()]，若内容为空，则无法提交
    username = StringField("Username", validators=[DataRequired()])

    password = PasswordField("Password",validators=[DataRequired()])

    # 布尔属性，即勾选框
    remember_me = BooleanField("Remember?")

    # 提交按钮，若username与password为空时点击submit则视为get请求
    submit = SubmitField('Submit')