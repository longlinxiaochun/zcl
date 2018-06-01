# -*- coding:utf-8 -*-


class Room(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = []

    def go(self, direction):
        return self.paths.get(direction, None)

    def add_paths(self, paths):
        self.paths.update(paths)

# pycharm显示无法引用到的这些类，即使这些类都在工程中，
# 看看文件上方的import会发现对应的模块import不成功。
# 既然这些类都在工程中，那么import不成功就是因为路径没对应，
# 事实上是pycharm默认该项目的根目录为source目录，
# 所以import使用绝对路径而不是相对路径的话，
# 就会从项目的根目录中查找，而不是我们希望的其中的/src目录，所以import不成功


a = {'name': 'zhang', 'tall': 180}
print "Value: %s" % a.get('tall', None)