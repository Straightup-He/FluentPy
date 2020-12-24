#-*- coding = utf-8 -*-
#@Time : 2020/12/7 22:36
#@Author : straightup
"""
使用 functools.lru_cache 做备忘
lru -- Least Recently Used  表明缓存不会无限制增长
"""
# from clockdeco import clock
#
# @clock
# def fibonacci(n):
#     if n < 2:
#         return n
#     return fibonacci(n-2) + fibonacci(n-1)
#
# if __name__ == '__main__':
#     print(fibonacci(6))


# -------------- 使用缓存实现 ----------------
import functools
import time

from clockdeco import clock

@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__ == '__main__':
    t0 = time.time()
    print(fibonacci(100))
    print(time.time() - t0)
"""
[0.00000060s] fibonacci(0) -> 0
[0.00000050s] fibonacci(1) -> 1
[0.00006040s] fibonacci(2) -> 1
[0.00000100s] fibonacci(3) -> 2
[0.00007980s] fibonacci(4) -> 3
[0.00000070s] fibonacci(5) -> 5
[0.00009920s] fibonacci(6) -> 8
8
"""