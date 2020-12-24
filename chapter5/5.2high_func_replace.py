#-*- coding = utf-8 -*-
#@Time : 2020/12/3 7:40
#@Author : straightup
"""
高阶函数的替代品
"""
def fact(n):
    """返回n的阶乘"""
    return 1 if n < 2 else n*fact(n-1)

# ------------- 计算阶乘列表,map和filter与列表推导比较 -------------
l1 = list(map(fact, range(6)))
l2 = [fact(i) for i in range(6)]
# print(l1)  # [1, 1, 2, 6, 24, 120]
# print(l2)  # [1, 1, 2, 6, 24, 120]

l3 = list(map(fact, filter(lambda n: n % 2, range(6))))
l4 = [fact(i) for i in range(6) if i % 2]
# print(l3)  # [1, 6, 120]
# print(l4)  # [1, 6, 120]

# ------------- reduce -------------
from functools import reduce
from operator import add

# 计算0~99的和
res = reduce(add, range(100))
print(res)  # 4950

print(sum(range(100)))  # 4950

