# -*- coding: utf-8 -*-
from flask import jsonify
from flask import Blueprint
from flask_login import login_required

from business.master.task import Task
from business.master.task.forms import TaskAddForm, TaskEditForm, TaskDeleteForm, TaskRunForm
from common.decorator import make_response_with_headers

bp_task = Blueprint('bp_task', __name__)


@bp_task.route('/task/index', methods=['GET'], endpoint='task_index')
@login_required
def task_index():
    """索引任务"""
    response = Task.index_task()
    return make_response_with_headers(jsonify(response))


@bp_task.route('/task/add', methods=['post'], endpoint='task_add')
@login_required
def task_add():
    """添加任务"""
    form = TaskAddForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)
    task = form.data_parser()
    response = Task.add_task(task)

    return make_response_with_headers(jsonify(response))


@bp_task.route('/task/edit', methods=['post'], endpoint='task_edit')
@login_required
def task_edit():
    """编辑任务"""
    form = TaskEditForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)
    task = form.data_parser()
    response = Task.edit_task(task)

    return make_response_with_headers(jsonify(response))


@bp_task.route('/task/run', methods=['post'], endpoint='task_run')
@login_required
def task_run():
    """执行任务"""
    form = TaskRunForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)
    action = form.data_parser()

    response = Task.run_task(action)

    return make_response_with_headers(jsonify(response))


@bp_task.route('/task/delete', methods=['post'], endpoint='task_delete')
@login_required
def task_delete():
    """删除任务"""
    form = TaskDeleteForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)

    response = Task.delete_task(form)
    return make_response_with_headers(response)
