import asyncio
from aiohttp import ClientSession

from business.master.activity import Activity
from common import st_instance
from common.st_flog import info_normal
from pickle_data.pickles import pick_task
from common.pick import Pickled
from common.decorator import data_paging


async def fn_run(a_id, node, task, proxy):
    if node not in st_instance.ins_node:
        return

    url = node + '/run'

    async with ClientSession() as session:
        try:
            code = st_instance.ins_task[task]['code']
            data = {'activity_id': a_id, 'code': code, 'task': task, 'proxy': proxy}
            async with session.post(url, data=data) as resp:
                rsp = await resp.json()
                if 'status' in rsp:
                    st_instance.ins_activity[a_id]['status'] = rsp['status']
                else:
                    st_instance.ins_activity[a_id]['status'] = '执行失败'
        except Exception as e:
            st_instance.ins_activity[a_id]['status'] = '执行失败'


class Task(Pickled):
    # 任务
    
    pick_ = pick_task
    KEY_NAME = 'task'
    
    def __init__(self, key, value):
        super(Pickled, self).__init__()
        self.key = key
        self.id = key
        
        self.value = value
        self.value.update({'key': key,
                           'version': 1})

    @classmethod
    def add_task(cls, task):
        """添加任务"""
        c = Task(**task)
        c.add()
        st_instance.ins_task = Task.loads()
        return {'status': True, 'messages': '添加成功', 'task': task}

    @classmethod
    def edit_task(cls, task):
        """编辑任务"""
        tasks = cls.loads()
        name = task['name']
        name_new = task['name_new']
        code = task['code']

        t = tasks.pop(name)
        t['name'] = name_new
        t['code'] = code
        t['key'] = name_new

        cls.remove(name)

        n = Task(key=name_new, value=t)
        n.add()
        st_instance.ins_task = Task.loads()
        return {'status': True, 'messages': '编辑成功', 'task': task}

    @classmethod
    def delete_task(cls, form):
        """删除任务"""
        success, defeat = cls.delete(form.get_ivs())
        st_instance.ins_task = cls.loads()
        return {'status': False if defeat else True, 'success': success, 'defeat': defeat}

    @classmethod
    def run_task(cls, action):
        """执行任务"""
        task = action['task']
        nodes = action['node']
        proxy = action['proxy']
        asyncio.set_event_loop(asyncio.new_event_loop())

        tasks = []
        for node in nodes:
            a_id = Activity.create(task, node, proxy)
            t = asyncio.ensure_future(fn_run(a_id, node, task, proxy))
            tasks.append(t)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        st_instance.ins_task[task]['run'] += 1
        return {'status': True, 'messages': '执行成功', 'task': action}

    @classmethod
    def index_task(cls):
        """索引任务"""
        task = {}
        task.update(st_instance.ins_task)

        total, rows = data_paging(task, cls.KEY_NAME)

        info_normal(
            m='rows',
            lo={'total': total},
            func='index_task'
        )
        for i, row in enumerate(rows):
            row['i'] = i + 1
        return {'rows': rows, 'total': total, 'status': True}
