#-*- coding = utf-8 -*-
#@Time : 2020/12/28 21:01
#@Author : straightup

from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)

# 测试
coro_avg = averager()
next(coro_avg)
coro_avg.send(10)
coro_avg.send(30)
coro_avg.send(6.5)
"""
# 普通版，返回值在异常中显示
coro_avg.send(None)

Traceback (most recent call last):
  ...
StopIteration: Result(count=3, average=15.5)
"""
# 捕获异常版
try:
    coro_avg.send(None)
except StopIteration as exc:
    result = exc.value
print(result)   # Result(count=3, average=15.5)



