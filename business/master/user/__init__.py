
from flask import session as f_session
from flask import g
from flask_login import login_user, logout_user, current_user

from common import st_instance
from common.st_flog import info_normal
from pickle_data.pickles import pick_user
from common.pick import Pickled
from common.decorator import data_paging


class User(Pickled):
    # 用户
    
    pick_ = pick_user
    is_authenticated = True
    is_active = True
    is_anonymous = False
    STATUS_BLOCK = 1
    STATUS_ACTIVE = 2
    KEY_NAME = 'account'

    def __init__(self, key, value):
        super(Pickled, self).__init__()
        self.key = key
        self.id = key
        self.value = value
        self.value.update({'status': self.STATUS_ACTIVE,
                           'key': key,
                           'version': 1})

    @classmethod
    def get_user(cls, user):
        return User(user, st_instance.ins_user[user]) if user in st_instance.ins_user else None

    def get_id(self):
        """
        get id
        :return: user.id
        """
        return self.id

    @classmethod
    def register_user(cls, form):
        """注册用户"""
        items = form.data_parser()
        user = User(*items)
        user.add()
        return {'status': True, 'message': '注册成功'}

    @classmethod
    def login_user(cls, form):
        """登录用户"""
        login_user(User.get_user(form.account.data), remember=True, fresh=True)
        g.user = current_user
        f_session['user_name'] = form.account.data
        return {'status': True, 'message': '登录成功'}

    @classmethod
    def logout_user(cls):
        """登出用户"""
        logout_user()
        return {'status': True}

    @classmethod
    def index_user(cls):
        """索引用户"""
        user = {}
        user.update(st_instance.ins_user)

        total, rows = data_paging(user, cls.KEY_NAME, exclude=['password'])

        info_normal(
            m='rows',
            lo={'total': total},
            func='index_user'
        )
        for i, row in enumerate(rows):
            row['i'] = i + 1
        return {'rows': rows, 'total': total, 'status': True}

    @classmethod
    def delete_user(cls, form):
        """删除用户"""
        success, defeat = cls.delete(form.get_ivs())
        return {'status': False if defeat else True, 'success': success, 'defeat': defeat}
