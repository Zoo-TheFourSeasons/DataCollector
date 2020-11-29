from common import st_instance
from common.st_flog import info_normal
from pickle_data.pickles import pick_proxy
from common.pick import Pickled
from common.decorator import data_paging


class Proxy(Pickled):
    # 代理

    pick_ = pick_proxy
    KEY_NAME = 'proxy'
    
    def __init__(self, key, value):
        super(Pickled, self).__init__()
        self.key = key
        self.id = key
        
        self.value = value
        self.value.update({'key': key,
                           'version': 1})

    @classmethod
    def add_proxy(cls, proxy):
        """添加代理"""
        Proxy.add_many(proxy.items())
        st_instance.ins_proxy = Proxy.loads()
        return {'status': True, 'messages': '添加成功', 'proxy': proxy}

    @classmethod
    def check_proxy(cls, proxy):
        """检测代理"""
        pass

    @classmethod
    def delete_proxy(cls, form):
        """删除代理"""
        success, defeat = cls.delete(form.get_ivs())
        st_instance.ins_proxy = cls.loads()
        return {'status': False if defeat else True, 'success': success, 'defeat': defeat}

    @classmethod
    def index_proxy(cls):
        """索引代理"""
        proxy = {}
        proxy.update(st_instance.ins_proxy)

        total, rows = data_paging(proxy, cls.KEY_NAME, fields=['proxy', 'status'])

        info_normal(
            m='rows',
            lo={'total': total},
            func='index_proxy'
        )
        for i, row in enumerate(rows):
            row['i'] = i + 1
        return {'rows': rows, 'total': total, 'status': True}
