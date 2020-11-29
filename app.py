# -*- coding: utf-8 -*-
"""app
"""
import pickle
import os
import traceback

from flask import jsonify
from flask import render_template
from flask import request
from flask import Flask
# from flask_socketio import SocketIO

from business.master.activity import Activity
from extensions import register_ext
from configuration.read import app_config
from business.master.cipher import Cipher
from business.master.node import Node
from business.master.proxy import Proxy
from business.master.task import Task
from business.master.user import User
from pickle_data.pickles import picks
from business.node.master import Master
from common import st_instance


def create_app(service_type):
    """create app
    """
    app = Flask(__name__)
    app.debug = False
    if service_type == 'master':
        app.template_folder = 'templates/master'
    else:
        app.template_folder = 'templates/node'
    app.secret_key = app_config['app']['secret-key']
    app.config.update(
        WTF_CSRF_SECRET_KEY=app_config['app']['secret-key'],
        WTF_CSRF_TIME_LIMIT=int(app_config['app']['csrf-time']),
        WTF_CSRF_ENABLED=app_config['app'].getboolean('csrf-enable'),

        PERMANENT_SESSION_LIFETIME=int(app_config['app']['session-time']),
        SESSION_REFRESH_EACH_REQUEST=app_config['app'].getboolean('session-refresh'),

        SEND_FILE_MAX_AGE_DEFAULT=int(app_config['app']['max-age']),
        FLASK_DB_QUERY_TIMEOUT=float(app_config['app']['query-time'])
    )
    register_ext(app)

    @app.errorhandler(Exception)
    def internal_error(error):
        traces = traceback.format_exc()
        print(traces)
        code = error.code
        if request.accept_mimetypes.best in \
                ('application/json', 'text/javascript', 'text/plain'):
            return jsonify({'status': False, 'message': str(error), 'traces': traces}), code
        else:
            return render_template('business/500.html', **locals()), code

    @app.before_request
    def before():
        """before
        """
        pass

    @app.before_first_request
    def init_pickle_file():
        for pick in picks:
            if isinstance(pick, (tuple, list)):
                for p in pick:
                    if not os.path.isfile(p):
                        with open(p, 'wb') as f:
                            pickle.dump({}, f)
            else:
                if not os.path.isfile(pick):
                    with open(pick, 'wb') as f:
                        pickle.dump({}, f)

    @app.before_first_request
    def init_st_instance():
        # init node
        # port = 9755
        # for i in range(1024):
        #     key = 'http://127.0.0.1:%s' % (port + i)
        #     value = {'key': key, 'name': 'node%s' % i, 'status': '激活', 'add_time': datetime.datetime.now()}
        #     node = Node(key, value)
        #     node.add()
        #
        # # init proxy
        # for i in range(255):
        #     key = '125.125.125.%s' % i
        #     value = {'key': key, 'proxy': key, 'add_time': datetime.datetime.now(),
        #              'version': 1,
        #              'status': '未知', 'business': []}
        #     proxy = Proxy(key, value)
        #     proxy.add()
        st_instance.ins_user = User.loads(amount=None)
        st_instance.ins_cipher = Cipher.loads()
        st_instance.ins_node = Node.loads()
        st_instance.ins_task = Task.loads()
        st_instance.ins_proxy = Proxy.loads()
        st_instance.ins_master = Master.loads()
        st_instance.ins_activity = Activity.loads()

    @app.teardown_request
    def shutdown_session(exception=None):
        pass

    # socket_io = SocketIO(
    #     app,
    #     async_mode=app_config['web-socket']['async-mode'],
    #     ping_timeout=int(app_config['web-socket']['ping-timeout']),
    #     ping_interval=int(app_config['web-socket']['ping-interval'])
    # )

    # return socket_io, app
    return None, app
