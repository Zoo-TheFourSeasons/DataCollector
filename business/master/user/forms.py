
import pickle
import hashlib

from wtforms import StringField
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import ValidationError

from pickle_data.pickles import pick_user
from common.form import IVsForm


class UserRegisterForm(FlaskForm):
    # 账户
    account = StringField('account',
                          [validators.required(message="账户必填")])
    # 密码
    password = StringField('password',
                           [validators.required(message='密码必填')])
    # 密码确认
    confirm = StringField('confirm',
                          [validators.required(message='确认密码必填')])

    @staticmethod
    def validate_account(form, field):
        if form.password.data != form.confirm.data:
            raise ValidationError('密码不一致')
        with open(pick_user, 'rb') as f:
            users = pickle.load(f)
            if field.data in users:
                raise ValidationError('账户已经存在: %s.' % field.data)

    def data_parser(self):
        sha = hashlib.sha512()
        sha.update(self.password.data.encode('utf-8'))
        return self.account.data, {'password': sha.digest(), 'key': self.account.data, 'is_active': True}


class UserLoginForm(FlaskForm):
    # 账户
    account = StringField('account',
                          [validators.required(message="账户必填")])
    # 密码
    password = StringField('password',
                           [validators.required(message='密码必填')])

    @staticmethod
    def validate_account(form, field):
        with open(pick_user, 'rb') as f:
            users = pickle.load(f)
            if field.data not in users:
                raise ValidationError('账户不存在或密码错误')

            sha = hashlib.sha512()
            sha.update(form.password.data.encode('utf-8'))
            if users[field.data]['password'] != sha.digest():
                raise ValidationError('账户不存在或密码错误')


class UserDeleteForm(IVsForm):

    def validate_ids(self, _):
        pass
