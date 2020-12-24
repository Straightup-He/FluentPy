#-*- coding = utf-8 -*-
#@Time : 2020/12/3 7:24
#@Author : straightup
"""
把函数视作对象
"""
def factorial(n):
    """返回n的阶乘"""
    return 1 if n < 2 else n*factorial(n-1)


print(factorial(3))         # 6
print(factorial.__doc__)    # 返回n的阶乘
print(type(factorial))      # <class 'function'> (function类的实例)

# 将函数赋值给变量,变量()执行
fact = factorial
print(fact)         # <function factorial at 0x000002C7D413D268>
print(fact(3))      # 6

# 将函数作为参数传递给map函数
print(map(factorial, range(5)))  # <map object at 0x0000017A900B0828>
print(list(map(factorial, range(5))))  # [1, 1, 2, 6, 24]


