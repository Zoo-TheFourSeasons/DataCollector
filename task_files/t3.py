# -*-coding: utf-8 -*-


class Collection(object):

    def start(self, node, proxy):
        """
        收集数据
        :param node: if not None: 使用的节点
        :param proxy: if not None: 使用的代理
        """
        pass

    def config(self):
        """
        爬虫的配置
        """
        self.running_times = 1
        self.start_time= None

