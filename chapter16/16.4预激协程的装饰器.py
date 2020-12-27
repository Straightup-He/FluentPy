#-*- coding = utf-8 -*-
#@Time : 2020/12/27 15:15
#@Author : straightup

from functools import wraps

def coroutine(func):
    """装饰器：向前执行到第一个`yield`表达式，预激`func`"""
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return primer

# @coroutine装饰器的用法
@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count

# 测试计算移动平均值的协程
coro_avg = averager()
from inspect import getgeneratorstate
print(getgeneratorstate(coro_avg))  # GEN_SUSPENDED

print(coro_avg.send(10))
print(coro_avg.send(30))
print(coro_avg.send(5))
"""
10.0
20.0
15.0
"""