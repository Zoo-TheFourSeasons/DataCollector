# -*- coding: utf-8 -*-

from flask import jsonify
from flask import Blueprint
from flask_login import login_required

from business.master.proxy import Proxy
from business.master.proxy.forms import ProxyAddForm, ProxyDeleteForm
from common.decorator import make_response_with_headers

bp_proxy = Blueprint('bp_proxy', __name__)


@bp_proxy.route('/proxy/index', methods=['GET'], endpoint='proxy_index')
@login_required
def proxy_index():
    """索引代理"""
    response = Proxy.index_proxy()
    return make_response_with_headers(jsonify(response))


@bp_proxy.route('/proxy/add', methods=['post'], endpoint='proxy_add')
def proxy_add():
    """添加代理"""
    form = ProxyAddForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)
    proxy = form.data_parser()
    response = Proxy.add_proxy(proxy)

    return make_response_with_headers(jsonify(response))


@bp_proxy.route('/proxy/delete', methods=['post'], endpoint='proxy_delete')
def proxy_delete():
    """删除代理"""
    form = ProxyDeleteForm()
    if not form.validate():
        errors = [','.join(form.errors[key]) for key in form.errors]
        response = jsonify({'status': False, 'messages': errors})
        return make_response_with_headers(response)

    response = Proxy.delete_proxy(form)
    return make_response_with_headers(response)
