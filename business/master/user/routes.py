# -*- coding: utf-8 -*-

from flask import jsonify
from flask import Blueprint
from flask_login import login_required

from common.decorator import make_response_with_headers
from business.master.user.forms import UserRegisterForm, UserLoginForm, UserDeleteForm
from business.master.user import User


bp_user = Blueprint('bp_user', __name__)


@bp_user.route('/user/register',
               methods=['POST'], endpoint='user_register')
def user_register():
    """注册用户"""
    form = UserRegisterForm()
    if not form.validate():
        response = {'status': False, 'messages': form.errors}
    else:
        response = User.register_user(form)
    return make_response_with_headers(jsonify(response))


@bp_user.route('/user/login', methods=['POST'], endpoint='user_login')
def user_login():
    """登录用户"""
    form = UserLoginForm()
    if not form.validate():
        response = {'status': False, 'messages': form.errors}
        return make_response_with_headers(response)
    else:
        response = User.login_user(form)
    return make_response_with_headers(jsonify(response))


@bp_user.route('/user/logout',
               methods=['GET'], endpoint='user_logout')
@login_required
def user_logout():
    """登出用户"""
    response = User.logout_user()
    return make_response_with_headers(jsonify(response))


@bp_user.route('/user/index', methods=['GET'], endpoint='user_index')
@login_required
def user_index():
    """索引用户"""
    response = User.index_user()
    return make_response_with_headers(jsonify(response))


@bp_user.route('/user/delete', methods=['post'], endpoint='user_delete')
@login_required
def user_delete():
    """删除用户"""
    form = UserDeleteForm()
    if not form.validate():
        response = {'status': False, 'messages': form.errors}
    else:
        response = User.delete_user(form)
    return make_response_with_headers(jsonify(response))
