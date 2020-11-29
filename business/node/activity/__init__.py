import random
from string import ascii_letters
import datetime

from common import st_instance
from common.st_flog import info_normal
from pickle_data.pickles import pick_activity
from common.pick import Pickled
from common.decorator import data_paging


class Activity(Pickled):
    # 节点上的活动

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
    def update_activity(cls):
        activity = ''.join([random.sample(ascii_letters, 1)[0] for _ in range(32)])
        start = datetime.datetime.now()
        invalid = start + datetime.timedelta(minutes=15)
        items = {
            'key': activity,
            'value': {
                'effective_time': str(start) + '-',
                'activity': activity
            },

        }
        cls.clean()
        c = Activity(**items)
        c.add()
        st_instance.ins_activity = Activity.loads()
        return {'status': True, 'messages': '更新成功', 'activity': activity}

    @classmethod
    def index_activity(cls):
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
