#-*- coding = utf-8 -*-
#@Time : 2020/12/27 10:00
#@Author : straightup

def simple_coroutine():
    print('-> coroutine started')
    x = yield
    print('-> coroutine received:', x)

my_coro = simple_coroutine()
print(my_coro)  # <generator object simple_coroutine at 0x0000012AD1A7BE58>

next(my_coro)
my_coro.send(42)
"""
-> coroutine started

-> coroutine received: 42
Traceback (most recent call last):
  File "C:/Users/harris/Desktop/fluentPy/chapter16/16.1协程展示.py", line 14, in <module>
    my_coro.send(42)
StopIteration
"""

