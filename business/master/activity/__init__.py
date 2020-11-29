import datetime
import time

from common import st_instance
from common.st_flog import info_normal
from pickle_data.pickles import pick_activity
from common.pick import Pickled
from common.decorator import data_paging


class Activity(Pickled):
    # 主控上的活动

    pick_ = pick_activity
    KEY_NAME = 'activity'
    
    def __init__(self, key, value):
        super(Pickled, self).__init__()
        self.key = key
        self.id = key
        
        self.value = value
        self.value.update({'key': key,
                           'version': 1})

    @classmethod
    def create(cls, task, node, proxy):
        """创建活动"""
        a_id = str(time.ctime())
        while a_id in st_instance.ins_activity:
            a_id = str(time.ctime())
        a = Activity(key=a_id, value={'key': a_id,
                                      'task': task,
                                      'node': node,
                                      'proxy': proxy,
                                      'add_time': datetime.datetime.now(),
                                      'status': '未执行',
                                      'version': 1})
        a.add()
        st_instance.ins_activity = Activity.loads()
        return a_id

    @classmethod
    def index_activity(cls):
        """索引活动"""
        activity = {}
        activity.update(st_instance.ins_activity)

        total, rows = data_paging(activity, cls.KEY_NAME)

        info_normal(
            m='rows',
            lo={'total': total},
            func='index_activity'
        )
        for i, row in enumerate(rows):
            row['i'] = i + 1
        return {'rows': rows, 'total': total, 'status': True}
