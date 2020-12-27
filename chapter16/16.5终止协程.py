#-*- coding = utf-8 -*-
#@Time : 2020/12/27 15:49
#@Author : straightup
"""
学习在协程中处理异常的测试代码
"""

class DemoException(Exception):
    """为这次演示定义的异常类型。"""

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> coroutine received: {!r}'.format(x))
    raise RuntimeError('This line should never run.')

# 最后一行：This code is unreachable（永远不会执行...）因为只有未处理的异常才会终止那个无限循环，而一旦出现未处理的异常，协程亦随之终止。

# 测试 demo_exc_handling 函数
# ------------- 激活和关闭 demo_exc_handling，没有异常 -------------
# exc_coro = demo_exc_handling()
# next(exc_coro)  # -> coroutine started
# exc_coro.send(11)  # -> coroutine received: 11
# exc_coro.send(22)  # -> coroutine received: 22
#
# exc_coro.close()
# from inspect import getgeneratorstate
# print(getgeneratorstate(exc_coro))  # GEN_CLOSED

# ------------- 把 DemoException 异常传入 demo_exc_handling 不会导致协程终止 -------------
# exc_coro = demo_exc_handling()
# next(exc_coro)  # -> coroutine started
# exc_coro.send(11)  # -> coroutine received: 11
# exc_coro.throw(DemoException)
# """
# *** DemoException handled. Continuing...
# """
# from inspect import getgeneratorstate
# print(getgeneratorstate(exc_coro))  # GEN_SUSPENDED

# ------------- 如果传入协程的异常没有处理，会导致协程终止 -------------
exc_coro = demo_exc_handling()
next(exc_coro)  # -> coroutine started
exc_coro.send(11)  # -> coroutine received: 11
exc_coro.throw(ZeroDivisionError)  # 报错！
"""
Traceback (most recent call last):
    ...
ZeroDivisionError
"""
from inspect import getgeneratorstate
print(getgeneratorstate(exc_coro))  # GEN_CLOSED


