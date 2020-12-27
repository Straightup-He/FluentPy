#-*- coding = utf-8 -*-
#@Time : 2020/12/27 10:20
#@Author : straightup

def simple_coro2(a):
    print('-> started: a =', a)
    b = yield a
    print('-> received: b =', b)
    c = yield a+b
    print('-> received: c =', c)

my_coro2 = simple_coro2(14)

from inspect import getgeneratorstate
print(getgeneratorstate(my_coro2))  # GEN_CREATED

next(my_coro2)
"""
-> started: a = 14
14
"""

print(getgeneratorstate(my_coro2))  # GEN_SUSPENDED

print(my_coro2.send(28))
"""
-> received: b = 28
42
"""
print(my_coro2.send(99))
"""
-> received: c = 99
Traceback (most recent call last):
  File "C:/Users/harris/Desktop/fluentPy/chapter16/16.2产出两个值的协程.py", line 23, in <module>
    my_coro2.send(99)
StopIteration
"""
print(getgeneratorstate(my_coro2))  # GEN_CLOSED
