# -*- coding: utf-8 -*-
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint
from flask import session as f_session
from flask_login import logout_user
from flask_login import login_required
from jinja2.exceptions import TemplateNotFound

from common.st_flog import error_un_excepted

rf_front = Blueprint('rf_front', __name__)


@rf_front.route('/', methods=['get'], endpoint='/')
def login():
    """登录页面跳转"""
    return redirect(url_for('rf_front.login_html'))


@rf_front.route('/s/register.html', methods=['get'],
                defaults={'target': 'register.html'}, endpoint='register_html')
@rf_front.route('/s/login.html', methods=['get'],
                defaults={'target': 'login.html'}, endpoint='login_html')
def login(target):
    """登录页面"""
    return render_template(target, **locals())


@rf_front.route('/s/<string:target>', defaults={'module': ''},
                methods=['get'], endpoint='without_module')
@rf_front.route('/s/<string:module>/<string:target>',
                methods=['get'], endpoint='with_module')
@login_required
def load_target(module, target):
    """索引"""
    lo = {'target': target,
          'module': module,
          }

    if 'user_name' not in f_session or not f_session['user_name']:
        error_un_excepted(
            m='用户未登录',
            lo=lo,
            func='load_target'
        )
        return redirect(url_for('rf_front.login_html'))

    try:
        __target = module + '/' + target if module else target
        return render_template(__target)
    except TemplateNotFound as e:
        error_un_excepted(
            m='页面不存在: %s, %s' % (request.path, e),
            lo=lo,
            func='load_target'
        )
        return redirect(url_for('rf_front.login_html'))


@rf_front.route("/sign_out")
@login_required
def sign_out():
    """用户退出
    跳转到登录页面
    """
    logout_user()
    return redirect(url_for('rf_front.login_html'))
