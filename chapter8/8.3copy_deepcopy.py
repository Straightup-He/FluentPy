#-*- coding = utf-8 -*-
#@Time : 2020/12/8 23:43
#@Author : straightup
"""
为任意对象做深复制和浅复制
"""
import copy

class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


bus1 = Bus(["Alice", "Bill", "Claire", "David"])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)
print(id(bus1), id(bus2), id(bus3))
# 2476561331424 2476561330640 2476561376760

bus1.drop('Bill')
print(bus2.passengers)  # ['Alice', 'Claire', 'David']
print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))
# 2285356641352 2285356641352 2285356565960
# bus1 和 bus2 的乘客id是一样的

print(bus3.passengers)  # ['Alice', 'Bill', 'Claire', 'David']

# 循环引用 进入无限循环
a = [10, 20]
b = [a, 30]
a.append(b)
print(a)  # [10, 20, [[...], 30]]

from copy import deepcopy
c = deepcopy(a)
print(c)  # [10, 20, [[...], 30]]

"""
l1 = [1, 2, 3]
print(id(l1))  # 2855995581256
l1 += [1, 2, 3]
print(id(l1))  # 2855995581256

t2 = (1, 2, 3)
print(id(t2))  # 2855996394304
t2 += (4, 5)
print(l1, t2)  # [1, 2, 3, 1, 2, 3] (1, 2, 3, 4, 5)
print(id(t2))  # 2855998244472
"""

