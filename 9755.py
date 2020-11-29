# -*- coding: utf-8 -*-
"""9755"""

import argparse

from app import create_app
from blueprints import register_bp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # 端口
    parser.add_argument('--port', help='端口. ',
                        type=int, default=9755)
    # 服务类型
    parser.add_argument('--type', help='服务类型. ',
                        type=str, default='node')

    args = parser.parse_args()

    print('应用端口:', args.port)

    socket_io, app = create_app(args.type)
    register_bp(app, service_type=args.type)

    # signal only works in main thread
    # socket_io.run(app, host='0.0.0.0', port=args.port, use_reloader=False)
    app.run(host='0.0.0.0', port=args.port, use_reloader=False)
