#-*- coding = utf-8 -*-
#@Time : 2020/12/28 21:27
#@Author : straightup

"""
yield from 计算平均值并输出统计报告
"""
from collections import namedtuple

Result = namedtuple('Result', 'count average')

# 子生成器
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)


# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from averager()


#客户端代码，即调用方
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)  # !!!若子生成器不终止，委派生成器将在yield from永远暂停
    print(results)
    report(results)


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit
        ))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.3, 41.7],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.3, 41.4],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48],
}

if __name__ == '__main__':
    main(data)

"""
{'girls;kg': Result(count=6, average=42.15), 'girls;m': Result(count=6, average=1.4349999999999998), 'boys;kg': Result(count=6, average=41.41666666666667), 'boys;m': Result(count=6, average=1.3833333333333335)}
 6 boys  averaging 41.42kg
 6 boys  averaging 1.38m
 6 girls averaging 42.15kg
 6 girls averaging 1.43m
"""