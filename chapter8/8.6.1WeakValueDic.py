#-*- coding = utf-8 -*-
#@Time : 2020/12/9 21:00
#@Author : straightup
"""
WeakValueDictionary
是一个类,实现的是一种可变映射,里面的值是对象的弱引用
被引用的对象在程序的其他地方被当做垃圾回收以后,对应的键会自动从中删除
因此其经常用于缓存
"""
class Cheese:
    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return 'Cheese(%r)' % self.kind

import weakref

stock = weakref.WeakValueDictionary()

catalog = [Cheese('Red Leicester'), Cheese('Tilsit'), Cheese('Brie'), Cheese('Parmesan')]
for cheese in catalog:
    stock[cheese.kind] = cheese

print(sorted(stock.keys()))  # ['Brie', 'Parmesan', 'Red Leicester', 'Tilsit']
del catalog
print(sorted(stock.keys()))  # ['Parmesan']  cheese是全局变量!引用了Parmesan
del cheese
print(sorted(stock.keys()))  # []
