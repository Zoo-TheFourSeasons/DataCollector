# -*- coding: utf-8 -*-

from flask import jsonify
from flask import Blueprint
from flask_login import login_required

from business.master.node import Node
from business.master.node.forms import NodeAddForm, NodeCheckForm
from common.decorator import make_response_with_headers

bp_node = Blueprint('bp_node', __name__)


@bp_node.route('/node/index', methods=['GET'], endpoint='node_index')
@login_required
def node_index():
    """索引节点"""
    response = Node.index_node()
    return make_response_with_headers(jsonify(response))


@bp_node.route('/node/register', methods=['post'], endpoint='node_register')
def node_register():
    """注册节点"""
    form = NodeAddForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)
    node = form.data_parser()
    response = Node.register_node(node)

    return make_response_with_headers(jsonify(response))


@bp_node.route('/node/check', methods=['post'], endpoint='node_check')
@login_required
def node_check():
    """检测节点"""
    form = NodeCheckForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)
    node = form.get_ids()
    response = Node.check_node(node)

    return make_response_with_headers(jsonify(response))
