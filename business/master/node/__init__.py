import asyncio
from aiohttp import ClientSession


from common import st_instance
from common.st_flog import info_normal
from pickle_data.pickles import pick_node
from common.pick import Pickled
from common.decorator import data_paging


async def fn_ping(node):
    """异步IO请求节点"""
    if node not in st_instance.ins_node:
        return

    url = node + '/ping'

    async with ClientSession() as session:
        try:
            print(url)
            async with session.get(url, timeout=2.1) as resp:
                print(resp)
                rsp = await resp.json()
                print(rsp)
                if 'status' in rsp:
                    st_instance.ins_node[node]['status'] = rsp['status']
                else:
                    st_instance.ins_node[node]['status'] = '断开'
        except Exception as e:
            print(e)
            st_instance.ins_node[node]['status'] = '断开'


class Node(Pickled):
    # 节点
    
    pick_ = pick_node
    KEY_NAME = 'node'
    
    def __init__(self, key, value):
        super(Pickled, self).__init__()
        self.key = key
        self.id = key
        
        self.value = value
        self.value.update({'key': key,
                           'version': 1})

    @classmethod
    def register_node(cls, node):
        """注册节点"""
        n = Node(**node)
        n.add()
        st_instance.ins_node = Node.loads()
        return {'status': True, 'messages': '添加成功', 'node': node}

    @classmethod
    def check_node(cls, nodes):
        """检测节点"""
        tasks = []
        asyncio.set_event_loop(asyncio.new_event_loop())
        for node in nodes:
            task = asyncio.ensure_future(fn_ping(node))
            tasks.append(task)

        print(len(tasks))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        print('dump')
        cls.dumps(st_instance.ins_node)
        return {'status': True, 'messages': '检测成功', 'node': nodes}

    @classmethod
    def index_node(cls):
        """索引节点"""
        node = {}
        node.update(st_instance.ins_node)

        total, rows = data_paging(node, cls.KEY_NAME, fields=['name', 'key', 'status'])

        info_normal(
            m='rows',
            lo={'total': total},
            func='index_node'
        )
        for i, row in enumerate(rows):
            row['i'] = i + 1
        return {'rows': rows, 'total': total, 'status': True}
