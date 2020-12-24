#-*- coding = utf-8 -*-
#@Time : 2020/12/4 8:58
#@Author : straightup
"""
同样可以冻结参数的 functools.partial
"""
from operator import mul
from functools import partial

triple = partial(mul, 3)
print(triple(7))    # 21
print(list(map(triple, range(1, 6))))  # [3, 6, 9, 12, 15]

