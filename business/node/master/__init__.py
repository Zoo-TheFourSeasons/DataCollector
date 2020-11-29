import importlib

from common import st_instance
from common.st_flog import info_normal
from pickle_data.pickles import pick_master
from common.pick import Pickled
from common.decorator import data_paging


class Collector(object):

    def __init__(self):
        pass

    def start(self):
        pass


class Master(Pickled):
    # 主控
    pick_ = pick_master
    KEY_NAME = 'master'

    def __init__(self, key, value):
        super(Pickled, self).__init__()
        self.key = key
        self.id = key

        self.value = value
        self.value.update({'key': key,
                           'version': 1})

    @classmethod
    def add_master(cls, master):
        """节点添加主控"""
        m = Master(**master)
        m.add()
        st_instance.ins_master = Master.loads()
        return {'status': True, 'messages': '添加成功', 'master': master}

    @classmethod
    def index_master(cls):
        """节点索引主控"""
        master = {}
        master.update(st_instance.ins_master)

        total, rows = data_paging(master, cls.KEY_NAME)

        info_normal(
            m='rows',
            lo={'total': total},
            func='index_master'
        )
        for i, row in enumerate(rows):
            row['i'] = i + 1
        return {'rows': rows, 'total': total, 'status': True}

    @classmethod
    def run(cls, action):
        """节点运行主控的任务"""
        task = action['task']
        code = action['code']
        proxy = action['proxy']

        with open('task_files/' + task + '.py', 'w', encoding='utf-8') as f:
            f.write(code)

        try:
            module = importlib.import_module('task_files.' + task)
            class_ = getattr(module, 'Collection')
            c = class_()
            c.start(None, proxy)

        except Exception as e:
            print(e)
            pass
        a = Collector()
        return {'status': True, 'messages': '执行中', 'action': action}
