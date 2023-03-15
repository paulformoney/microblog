from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import email_validator, ValidationError, DataRequired, EqualTo, Email, Length
from app.models import User


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


# 注册表单
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    # 二次输入密码，从wtforms.validators导入EqualTo，使用方法：参数2 = EqualTo('要校验的参数1','提示语句')，校验表单中两次的数据是否一致
    repeat_password = PasswordField('RepeatPassword', validators=[DataRequired(), EqualTo("password","password should be matched")])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # 提交表单为对象，使用对象.data获取属性
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('name has been register,please input another one')

    def valita_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('email has been register,please input another one')


# 编辑个人资料类，可修改用户名与个人简介
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('about_me ', validators=[Length(0, 140)])

    submit = SubmitField('Commit Edit')

    # # 验证用户名
    # def __init__(self, original_username, *args, **kwargs):
    #     super(EditProfileForm, self).__init__(*args, **kwargs)
    #     self.original_username = original_username
    #
    # def validate_username(self, username):
    #     if username.data != self.original_username:
    #         user = User.query.filter_by(username=self.username.data).first()
    #         if user is not None:
    #             raise ValidationError('Please use a different username.')