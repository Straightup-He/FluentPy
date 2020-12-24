#-*- coding = utf-8 -*-
#@Time : 2020/12/9 8:28
#@Author : straightup
"""
函数的参数作为引用时
"""
def f(a, b):
    a += b
    return a

x = 1
y = 2
f(x, y)
print(x, y)  # 1 2  不变

a = [1, 2]
b = [3, 4]
f(a, b)
print(a, b)  # [1, 2, 3, 4] [3, 4]  a发生改变!

t1 = (10, 20)
t2 = (30, 40)
f(t1, t2)
print(t1, t2)  # (10, 20) (30, 40)  元组不变

"""
lst = [1, 2, 3]
lst2 = list(lst)
lst.append(4)
print(lst, lst2)  # [1, 2, 3, 4] [1, 2, 3]
print(id(lst), id(lst2))  # 2198258333768 2198258444040
"""
