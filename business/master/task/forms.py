import datetime

from wtforms import StringField
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import ValidationError

from common import st_instance
from common.form import IVsForm


class TaskAddForm(FlaskForm):
    # 任务
    code = StringField('code',
                       [validators.required(message="代码必填")])
    name = StringField('name',
                       [validators.required(message="名称必填")])

    @staticmethod
    def validate_name(form, _):
        name = form.name.data
        if name in st_instance.ins_task:
            raise ValidationError('任务已存在: %s' % name)

    def data_parser(self):
        return {
            'key': self.name.data,
            'value': {'name': self.name.data,
                      'code': self.code.data.replace('\r', ''),
                      'run': 0,
                      'add_time': datetime.datetime.now()}
        }


class TaskEditForm(FlaskForm):
    # 任务
    code = StringField('code',
                       [validators.required(message="代码必填")])
    name = StringField('name',
                       [validators.required(message="名称必填")])
    name_new = StringField('name_new',
                           [validators.required(message="名称必填")])

    @staticmethod
    def validate_name(form, _):
        name_new = form.name_new.data
        name = form.name.data
        if name_new in st_instance.ins_task and name_new != name:
            raise ValidationError('任务已存在: %s' % name_new)

    def data_parser(self):
        return {'name': self.name.data,
                'code': self.code.data.replace('\r', ''),
                'name_new': self.name_new.data}


class TaskRunForm(FlaskForm):
    # 任务
    task = StringField('task',
                       [validators.required(message="任务必填")])
    node = StringField('node',
                       [validators.required(message="节点必填")])
    proxy = StringField('proxy',
                        [validators.optional()])

    @staticmethod
    def validate_task(form, _):
        nodes = form.node.data
        nodes = nodes.replace(' ', '').split(',')
        error = []
        for n in nodes:
            if n not in st_instance.ins_node:
                error.append(n)

        if error:
            raise ValidationError('节点不存在: %s' % ','.join(error))

    def data_parser(self):
        return {'task': self.task.data,
                'proxy': self.proxy.data.replace(' ', '').split(','),
                'node': self.node.data.replace(' ', '').split(',')}


class TaskDeleteForm(IVsForm):

    def validate_ids(self, _):
        pass
