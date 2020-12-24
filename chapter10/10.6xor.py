#-*- coding = utf-8 -*-
#@Time : 2020/12/12 23:03
#@Author : straightup
"""
计算整数0~5的累积异或的3种方式
"""
n = 0
for i in range(1, 6):
    n ^= i
print(n)

import functools
res = functools.reduce(lambda a, b: a ^ b, range(6))
print(res)

import operator
res = functools.reduce(operator.xor, range(6))
print(res)
