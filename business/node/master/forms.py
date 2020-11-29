import pickle
import datetime

from wtforms import StringField
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import ValidationError
import requests

from common.form import IVsForm


class MasterAddForm(FlaskForm):
    # 主控
    master = StringField('master',
                         [validators.required(message="主控必填")])
    cipher = StringField('cipher',
                         [validators.required(message="密钥必填")])
    name = StringField('name',
                       [validators.required(message="名称必填")])
    node = StringField('node',
                       [validators.required(message="节点地址必填")])

    @staticmethod
    def validate_master(form, _):
        data = {
            'cipher': form.cipher.data,
            'name': form.name.data,
            'master': form.master.data,
            'node': form.node.data
        }
        url = form.master.data + '/node/register'
        try:
            rsp = requests.post(url, data)
            r = rsp.json()
        except Exception as e:
            raise ValidationError('主控连接错误, 请检查主控地址: %s' % form.master.data)

        if 'status' not in r or not r['status']:
            raise ValidationError('主控响应错误: %s' % r)

    def data_parser(self):

        return {'key': self.master.data,
                'value': {
                    'cipher': self.cipher.data,
                    'node': self.node.data,
                    'name': self.name.data,
                    'master': self.master.data,
                    'add_time': datetime.datetime.now(),
                    'status': '活动'
                }}


class MasterRunForm(FlaskForm):
    # 代码
    activity_id = StringField('activity_id',
                       [validators.required(message="任务号必填")])
    code = StringField('code',
                       [validators.required(message="任务代码必填")])
    task = StringField('task',
                       [validators.required(message="任务必填")])
    proxy = StringField('proxy',
                        [validators.optional()])

    @staticmethod
    def validate_code(form, _):
        pass

    def data_parser(self):

        return {'code': self.code.data,
                'task': self.task.data,
                'activity_id': self.activity_id.data,
                'proxy': self.proxy.data.replace(' ', '').replace(',', ';').split(';')
                }


class MasterDeleteForm(IVsForm):

    def validate_ids(self, _):
        pass
