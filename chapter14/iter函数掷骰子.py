"""
使用 iter 函数掷骰子，直到掷出 1 点为止
"""
from random import randint

def d6():
    return randint(1, 6)

d6_iter = iter(d6, 1)
print(d6_iter)  # <callable_iterator object at 0x0000000002169198>

for roll in d6_iter:
    print(roll)
"""
3
6
4
因为 1 是哨符，肯定不会打印 1，
"""