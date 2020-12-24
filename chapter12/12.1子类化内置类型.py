#-*- coding = utf-8 -*-
#@Time : 2020/12/15 22:18
#@Author : straightup

class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


dd = DoppelDict(one=1)
print(dd)  # {'one': 1}

dd['two'] = 2
print(dd)  # {'one': 1, 'two': [2, 2]}

dd.update(three=3)
print(dd)  # {'one': 1, 'two': [2, 2], 'three': 3}

"""
只有[]赋值运算符生效了, 其余 __init__ 和 update 方法都忽略了我们覆盖的方法
"""
# ----------------------------------------------------------------
import collections

class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


ddd = DoppelDict2(one=1)
print(ddd)  # {'one': [1, 1]}

ddd['two'] = 2
print(ddd)  # {'one': [1, 1], 'two': [2, 2]}

ddd.update(three=3)
print(ddd)  # {'one': [1, 1], 'two': [2, 2], 'three': [3, 3]}

"""
继承collections.UserDict, 问题迎刃而解
"""
