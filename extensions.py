# -*- coding: utf-8 -*-
"""扩展"""
import pickle

from flask import jsonify
from flask import request
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import url_for

from common.decorator import make_response_with_headers
from pickle_data.pickles import pick_user
from business.master.user import User

login_manager = LoginManager()
login_manager.session_protection = 'strong'
# 跨站保护
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user):
    """加载用户"""
    with open(pick_user, 'rb') as f:
        users = pickle.load(f)
        return User(user, users[user]) if user in users else None


@login_manager.unauthorized_handler
def unauthorized():
    """未登录处理"""
    code = 403
    if request.accept_mimetypes.best in \
            ('application/json', 'text/javascript', 'text/plain'):
        return make_response_with_headers(jsonify({'status': False, 'message': '请先登录'})), code
    else:
        return redirect(url_for('rf_front.login_html'))


def register_ext(app):
    """注册扩展"""
    # 用户登录
    login_manager.init_app(app)

    csrf.init_app(app)
    app.__setattr__('csrf', csrf)
