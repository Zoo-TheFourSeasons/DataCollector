# # 函数级日志写 线程
# # 非进程间安全
# import time
# from threading import Thread
#
# from refactor import st_flog
# from refactor.st_flog import FLOG
# from refactor.rf_db_engine import db_session as current_session
#
#
# class FLogWriter(Thread):
#
#     def __init__(self):
#         super(FLogWriter, self).__init__()
#
#     def run(self):
#         while True:
#             while not st_flog.que.empty():
#                 log = st_flog.que.get()
#                 row = FLOG(**log)
#                 current_session.add(row)
#                 current_session.commit()
#
#             time.sleep(5)
