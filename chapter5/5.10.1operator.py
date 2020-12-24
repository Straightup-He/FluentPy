#-*- coding = utf-8 -*-
#@Time : 2020/12/3 22:51
#@Author : straightup
"""
函数式编程的包
operator
"""
"""
# 使用reduce函数和一个匿名函数计算阶乘
from functools import reduce

def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))
"""
# 使用reduce和operator.mul函数计算阶乘
from functools import reduce
from operator import mul

def fact(n):
    return reduce(mul, range(1, n+1))

# print(fact(5))  # 120

# methodcaller 自行创建函数
from operator import methodcaller

s = 'Winter is coming!'
upcase = methodcaller('upper')
print(upcase(s))  # WINTER IS COMING!
"""
upcase = methodcaller('uupper')
print(upcase(s))  # 报错 AttributeError: 'str' object has no attribute 'urpper'
"""

my_replace = methodcaller('replace', ' ', '-')
print(my_replace(s))  # Winter-is-coming!
print(s.replace(' ', '-'))  # Winter-is-coming!
