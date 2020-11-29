# # -*- coding: utf-8 -*-
# """
# FLOG路由
# """
#
# from flask import jsonify
# from flask import request
# from flask import Blueprint
# from flask_login import login_required
#
# from refactor.rf_db_engine import db_session as current_session
# from refactor.f_ import rf_query_data
# from refactor.st_flog import FLOG
#
# rf_flog = Blueprint('rf_flog', __name__, template_folder='templates')
#
#
# @rf_flog.route('/rf/flog/data', methods=['get'], endpoint='flog_data')
# @login_required
# def flog_data():
#     """
#     FLOG 索引数据
#     :return: json
#     """
#     query = current_session.query(FLOG)
#     # 筛选类型
#     if 'f_level' in request.args:
#         f_level = request.args['f_level']
#         query = query.filter(FLOG.f_level == int(f_level))
#     total, rows, offset = rf_query_data(request, query, FLOG)
#     rows_ = []
#     for i, row in enumerate(rows):
#         item = row.to_dict()
#         item['i'] = i + 1
#         rows_.append(item)
#     return jsonify({'total': total, 'rows': rows_})
#
#
# @rf_flog.route('/rf/flog/delete', methods=['post'], endpoint='delete')
# @login_required
# def flog_delete():
#     """
#     删除FLOG
#     :return: json
#     """
#     pass
#     # form = FLOGDeleteForm()
#     # if not form.validate():
#     #     response = {'status': False, 'message': form.errors}
#     #     return jsonify(trans_errors(response))
#     #
#     # ids = form.ids.data.split(',')
#     #
#     # current_session.query(FLOG).filter(FLOG.id.in_(ids)).delete(synchronize_session=False)
#     # current_session.commit()
#     #
#     # return jsonify({'status': True, 'message': '删除成功.'})
