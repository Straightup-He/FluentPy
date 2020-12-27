#-*- coding = utf-8 -*-
#@Time : 2020/12/7 8:21
#@Author : straightup
"""
用类实现 avg
"""
class Averager:
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)

# avg = Averager()
# print(avg(10))      # 10.0
# print(avg(11))      # 10.5
# print(avg(12))      # 11.0


# ------------------------ 函数式实现 -------------------------
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager

# 每次调用 make_averager 都会返回一个 averager 函数对象,再加括号即可执行!
avg = make_averager()
print(avg(10))      # 10.0
print(avg(11))      # 10.5
print(avg(12))      # 11.0

print(avg.__code__.co_varnames)  # ('new_value', 'total')  局部变量
print(avg.__code__.co_freevars)  # ('series',)  自由变量

# 数据保存在这!
print(avg.__closure__)  # (<cell at 0x000001DF996228E8: list object at 0x000001DF99576248>,)
print(avg.__closure__[0].cell_contents)  # [10, 11, 12]


# ------------------------- 改进版 --------------------------------
# 不保存所有历史的版本
def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total/count
    return averager