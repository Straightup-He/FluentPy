#-*- coding = utf-8 -*-
#@Time : 2020/12/9 9:15
#@Author : straightup
"""
del和垃圾回收
"""
import weakref
s1 = {1, 2, 3}
s2 = s1
def bye():
    print('Gone with the wind...')

ender = weakref.finalize(s1, bye)
print(ender.alive)  # True
del s1
print(ender.alive)  # True
# 重新绑定s2的指向
s2 = 'Spam'
# Gone with the wind...
print(ender.alive)  # False
