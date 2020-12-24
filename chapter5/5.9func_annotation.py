#-*- coding = utf-8 -*-
#@Time : 2020/12/3 22:47
#@Author : straightup
"""
函数注解
"""
def clip(text:str, max_len:'int > 0'=80) -> str:
    pass

print(clip.__annotations__)
# {'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}
