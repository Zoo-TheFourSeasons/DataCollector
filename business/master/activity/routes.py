# -*- coding: utf-8 -*-

from flask import jsonify
from flask import Blueprint
from flask_login import login_required

from business.master.activity import Activity
from common.decorator import make_response_with_headers

bp_activity = Blueprint('bp_activity', __name__,
                        template_folder='templates')


@bp_activity.route('/activity/index', methods=['GET'], endpoint='activity_index')
@login_required
def activity_index():
    """索引活动"""
    response = Activity.index_activity()
    return make_response_with_headers(jsonify(response))
