# -*- coding: utf-8 -*-

from flask import jsonify
from flask import Blueprint
from flask_login import login_required

from business.node.master import Master
from business.node.master.forms import MasterAddForm, MasterRunForm
from common import st_instance
from common.decorator import make_response_with_headers

bp_master = Blueprint('bp_master', __name__)


@bp_master.route('/master/index', methods=['GET'], endpoint='master_index')
@login_required
def master_index():
    """节点索引主控"""
    response = Master.index_master()
    return make_response_with_headers(jsonify(response))


@bp_master.route('/master/add', methods=['post'], endpoint='master_add')
@login_required
def master_add():
    """节点添加主控"""
    form = MasterAddForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)
    master = form.data_parser()
    response = Master.add_master(master)

    return make_response_with_headers(jsonify(response))


@bp_master.route('/ping', methods=['get'], endpoint='master_ping')
def master_ping():
    """节点检测状态"""
    response = {
        'status': '在忙' if st_instance.ins_activity else '空闲'
    }
    return make_response_with_headers(jsonify(response))


@bp_master.route('/run', methods=['post'], endpoint='master_run')
def master_run():
    """节点运行主控的任务"""
    form = MasterRunForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)
    action = form.data_parser()
    response = Master.run(action)

    return make_response_with_headers(jsonify(response))
