#-*- coding = utf-8 -*-
#@Time : 2020/12/2 8:20
#@Author : straightup
"""
泛映射类型
"""
from collections import abc

my_dict = {}
print(isinstance(my_dict, dict))  # True
print(isinstance(my_dict, abc.Mapping))  # True

# 判断是否可散列,hash值
t1 = (1, 2, (3, 4))
t2 = (1, 2, [3, 4])
t3 = (1, 2, frozenset([30, 40]))
print(hash(t1))  # -2725224101759650258
# print(hash(t2))  # 报错!
print(hash(t3))  # 985328935373711578

# --------------- setdefault ---------------------
# 处理找不到键
my_dict = {}
for i in range(5):
    my_dict.setdefault('key1', []).append(1)
    print(my_dict)  # {'key1': [1, 1, 1, 1, 1]}
# 键存在
my_dict = {'key1': 6}
my_dict.setdefault('key1', 7)
print(my_dict)  # {'key1': 6}
