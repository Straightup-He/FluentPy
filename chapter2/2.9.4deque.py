#-*- coding = utf-8 -*-
#@Time : 2020/12/2 7:34
#@Author : straightup
"""
双向队列
"""
from collections import deque

dq = deque(range(10), maxlen=10)  # maxlen可容纳元素的最大数量
print(dq)  # deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)

# 旋转操作 n>0,右边的n个元素会移动到队列左边
dq.rotate(3)
print(dq)  # deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)

# 对满的队列做头部添加操作,另一端的元素会被挤掉
dq.appendleft(-1)
print(dq)  # deque([-1, 7, 8, 9, 0, 1, 2, 3, 4, 5], maxlen=10)

# 添加多个则挤掉多个
dq.extend([11, 22, 33])
print(dq)  # e([9, 0, 1, 2, 3, 4, 5, 11, 22, 33], maxlen=10)

# 参数为迭代器,一个一个添加,所以会出现逆序
dq.extendleft([10, 20, 30])
print(dq)  # deque([30, 20, 10, 9, 0, 1, 2, 3, 4, 5], maxlen=10)





