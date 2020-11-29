# -*- coding: utf-8 -*-
"""blueprints
"""

from business.master.front.routes import rf_front
from business.master.user.routes import bp_user
from business.master.cipher.routes import bp_cipher
from business.master.proxy.routes import bp_proxy
from business.master.node.routes import bp_node
from business.master.task.routes import bp_task
from business.node.master.routes import bp_master
from business.master.activity.routes import bp_activity
from business.node.activity.routes import bp_node_activity


def register_bp(app_, service_type):
    """register bp
    """
    app_.register_blueprint(rf_front)
    app_.register_blueprint(bp_user)
    if service_type == 'master':
        app_.register_blueprint(bp_cipher)
        app_.register_blueprint(bp_proxy)
        app_.register_blueprint(bp_node)
        app_.register_blueprint(bp_task)
        app_.register_blueprint(bp_activity)
    else:
        app_.register_blueprint(bp_master)
        app_.register_blueprint(bp_node_activity)
