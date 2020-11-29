import datetime

from wtforms import StringField
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import ValidationError

from common import st_instance
from common.form import IVsForm


class NodeAddForm(FlaskForm):
    # 主控
    node = StringField('node',
                       [validators.required(message="节点必填")])
    cipher = StringField('cipher',
                         [validators.required(message="密钥必填")])
    name = StringField('name',
                       [validators.required(message="名称必填")])

    @staticmethod
    def validate_master(form, _):
        cipher = form.cipher.data

        if cipher not in st_instance.ins_cipher:
            raise ValidationError('密钥错误: %s' % cipher)

        node = form.node.data
        if node in st_instance.ins_node:
            raise ValidationError('节点已存在: %s' % node)

    def data_parser(self):

        return {
            'key': self.node.data,
            'value': {'name': self.name.data,
                      'status': '活动',
                      'node': self.node.data,
                      'add_time': datetime.datetime.now(),
                      'cipher': self.cipher.data
                      }
        }


class NodeDeleteForm(IVsForm):

    def validate_ids(self, _):
        pass


class NodeCheckForm(IVsForm):

    def validate_ids(self, _):
        pass
