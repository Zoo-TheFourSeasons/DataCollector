# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """F-LOG管理表定义"""
# from sqlalchemy import Column
# from sqlalchemy import DateTime
# from sqlalchemy import Integer
# from sqlalchemy import String
# from sqlalchemy import JSON
# from sqlalchemy.dialects.mysql import LONGTEXT
# from sqlalchemy import or_
#
# from refactor.rf_db_engine import Base
# from refactor.rf_db_engine import engine


class FLOG(object):
    """
    FLOG
    """
    __tablename__ = 'flog'

    # 预期错误
    LEVEL_ERROR_EXCEPTED = 1
    # 意外错误
    LEVEL_ERROR_UN_EXCEPTED = 2
    # 普通消息
    LEVEL_INFO_NORMAL = 3
    # 重要的消息
    LEVEL_INFO_IMPORTANT = 4
    # 警告, 可能引起ERROR的地方
    LEVEL_WARN = 5

    LEVEL = {
        LEVEL_ERROR_EXCEPTED: '预期错误',
        LEVEL_ERROR_UN_EXCEPTED: '意外错误',
        LEVEL_INFO_NORMAL: '普通消息',
        LEVEL_INFO_IMPORTANT: '重要消息',
        LEVEL_WARN: '警告'
    }

#     id = Column(Integer, primary_key=True)
#     version = Column(Integer, default=1)
#     # 触发时间
#     f_time = Column(DateTime)
#     # 等级
#     f_level = Column(Integer, default=LEVEL_ERROR_UN_EXCEPTED)
#     # 消息体
#     f_message = Column(LONGTEXT, default='')
#     # 本地对象
#     f_local = Column(JSON, default={})
#     # 函数体
#     f_function = Column(String(128), default='')
#
#     @classmethod
#     def get_attr(cls, attr):
#         as_ = {'f_time': cls.f_time,
#                'f_level': cls.f_level,
#                'f_message': cls.f_message,
#                'f_function': cls.f_function,
#                'id': cls.id}
#         return as_[attr]
#
#     @classmethod
#     def get_filter(cls, value):
#         return or_(cls.f_time.contains(value),
#                    or_(cls.f_time.contains(value),
#                        cls.f_function.contains(value)))
#
#
# def create_f_log():
#     """创建表"""
#     Base.metadata.create_all(bind=engine)
#
#
# if __name__ == '__main__':
#     create_f_log()
