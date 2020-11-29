import pickle

from performance.meta import TimerMeta
from performance.decorator import func_timer


class Pickled(metaclass=TimerMeta):
    # 数据序列化存储

    pick_ = None

    def __init__(self, key, value):
        self.key = key
        self.value = value

    @classmethod
    @func_timer
    def loads(cls, amount=12, exclude=()):
        # 从文件反序列化数据
        def exclude_():
            for e in exclude:
                picks.pop(e, None)

        if isinstance(cls.pick_, (tuple, list)):
            picks = {}
            for file in cls.pick_:
                with open(file, 'rb') as f:
                    pick = pickle.load(f)
                    picks.update(pick)
                    exclude_()
                    if amount and len(picks) > amount:
                        return picks
        else:
            with open(cls.pick_, 'rb') as f:
                picks = pickle.load(f)

        exclude_()
        return picks

    @classmethod
    def dumps(cls, picks):
        # 数据序列化到文件
        if isinstance(cls.pick_, (tuple, list)):
            length = len(cls.pick_)
            picks_ = dict([(x, {}) for x in range(length)])
            i = 0
            for key in picks:
                picks_[i][key] = picks[key]
                i += 1
                i = i % length

            for i, key in enumerate(picks_.keys()):
                with open(cls.pick_[i], 'wb') as f:
                    pickle.dump(picks_[key], f, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open(cls.pick_, 'wb') as f:
                pickle.dump(picks, f, protocol=pickle.HIGHEST_PROTOCOL)

    def add_item(self, key, value):
        # 添加一项数据
        picks = self.loads()
        if key not in picks:
            picks[key] = value

        with open(self.pick_, 'wb') as f:
            pickle.dump(picks, f)

    def add(self):
        # 添加当前数据
        picks = self.loads()
        if self.key not in picks:
            picks[self.key] = self.value

        with open(self.pick_, 'wb') as f:
            pickle.dump(picks, f)

    @classmethod
    def clean(cls):
        # 清空数据
        with open(cls.pick_, 'wb') as f:
            pickle.dump({}, f)

    @classmethod
    def delete(cls, ivs):
        """
        删除数据
        :param cls: class
        :param ivs: tuple
        :return: success, defeat
        """
        defeat = []
        success = []
        picks = cls.loads()

        for id_, version in ivs:
            if id_ in picks and picks[id_]['version'] == version:
                picks.pop(id_, None)
                success.append(id_)
            else:
                defeat.append(id_)

        with open(cls.pick_, 'wb') as f:
            pickle.dump(picks, f)
        return success, defeat

    @classmethod
    def remove(cls, key):
        # 移除并返回数据
        picks = cls.loads()
        if key in picks:
            picks.pop(key, None)

        with open(cls.pick_, 'wb') as f:
            pickle.dump(picks, f)

    @classmethod
    def add_many(cls, items):
        # 添加多项数据
        picks = cls.loads()

        for key, value in items:
            if key not in picks:
                picks[key] = value

        with open(cls.pick_, 'wb') as f:
            pickle.dump(picks, f)
