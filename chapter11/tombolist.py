#-*- coding = utf-8 -*-
#@Time : 2020/12/14 22:54
#@Author : straightup
"""
Tombola的虚拟子类
"""
from random import randrange
from tombola import Tombola

@Tombola.register
class Tombolist(list):

    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty Tombolist')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))


t = Tombolist()

print(isinstance(t, Tombola))  # True
print(issubclass(Tombolist, Tombola))  # True

print(Tombolist.__mro__)
# (<class '__main__.Tombolist'>, <class 'list'>, <class 'object'>)
