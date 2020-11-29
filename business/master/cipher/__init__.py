import random
from string import ascii_letters
import datetime

from common import st_instance
from common.st_flog import info_normal
from pickle_data.pickles import pick_cipher
from common.pick import Pickled
from common.decorator import data_paging


class Cipher(Pickled):
    # 密钥
    
    pick_ = pick_cipher
    KEY_NAME = 'cipher'
    
    def __init__(self, key, value):
        super(Pickled, self).__init__()
        self.key = key
        self.id = key
        
        self.value = value
        self.value.update({'key': key,
                           'version': 1})

    @classmethod
    def update_cipher(cls):
        """更新密钥"""
        cipher = ''.join([random.sample(ascii_letters, 1)[0] for _ in range(32)])
        start = datetime.datetime.now()
        # invalid = start + datetime.timedelta(minutes=15)
        items = {
            'key': cipher,
            'value': {
                'effective_time': str(start) + '-',
                'cipher': cipher
            },

        }
        cls.clean()
        c = Cipher(**items)
        c.add()
        st_instance.ins_cipher = Cipher.loads()
        return {'status': True, 'messages': '更新成功', 'cipher': cipher}

    @classmethod
    def index_cipher(cls):
        """索引密钥"""
        cipher = {}
        cipher.update(st_instance.ins_cipher)

        total, rows = data_paging(cipher, cls.KEY_NAME)

        info_normal(
            m='rows',
            lo={'total': total},
            func='index_cipher'
        )
        for i, row in enumerate(rows):
            row['i'] = i + 1
        return {'rows': rows, 'total': total, 'status': True}
