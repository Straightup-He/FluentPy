#-*- coding = utf-8 -*-
#@Time : 2020/12/27 12:51
#@Author : straightup

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count

# 测试
coro_avg = averager()
# 首先激活协程
next(coro_avg)

print(coro_avg.send(10))  # 10.0
print(coro_avg.send(30))  # 20.0
print(coro_avg.send(5))   # 15.0


