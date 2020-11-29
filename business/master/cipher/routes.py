# -*- coding: utf-8 -*-

from flask import jsonify
from flask import Blueprint
from flask_login import login_required

from business.master.cipher import Cipher
from common.decorator import make_response_with_headers

bp_cipher = Blueprint('bp_cipher', __name__,
                      template_folder='templates')


@bp_cipher.route('/cipher/index', methods=['GET'], endpoint='cipher_index')
@login_required
def cipher_index():
    """索引密钥"""
    response = Cipher.index_cipher()
    return make_response_with_headers(jsonify(response))


@bp_cipher.route('/cipher/update', methods=['get'], endpoint='cipher_update')
@login_required
def cipher_update():
    """更新密钥"""
    response = Cipher.update_cipher()
    return make_response_with_headers(jsonify(response))
