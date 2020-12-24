#-*- coding = utf-8 -*-
#@Time : 2020/12/2 11:51
#@Author : straightup

import collections

# 如果找不到键,则默认生成一个空列表作为其的值
my_dict = collections.defaultdict(list)

print(my_dict['new_key'])  # []
print(my_dict)  # defaultdict(<class 'list'>, {'new_key': []})

# 整数计数器(可散列对象计数)
ct = collections.Counter('1112223456667')
print(ct)  # Counter({'1': 3, '2': 3, '6': 3, '3': 1, '4': 1, '5': 1, '7': 1})

# ------------------- collections.UserDict -------------------------
# 创建一个键一定是字符串的字典
class StrKeyDict(collections.UserDict):

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, value):
        """键以字符串的形式存储"""
        self.data[str(key)] = value

str_key_dict = StrKeyDict()
str_key_dict['key1'] = 'value1'
print(str_key_dict['key1'])  # value1
# print(str_key_dict[123])  # KeyError: '123'

