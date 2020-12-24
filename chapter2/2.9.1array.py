#-*- coding = utf-8 -*-
#@Time : 2020/12/1 23:28
#@Author : straightup
"""
在某些情况取代列表的数据结构
"""
# ------------------------ 数组array ---------------------------
# 需要一个只包含数字的列表
# 创建一个有1000万个随机浮点数的数组
from array import array
from random import random

floats = array('d', (random() for i in range(10**7)))
print(floats[-1])  # 0.8577432425578952

# 写入文件
fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()
# 从文件中读取
# 创建一个双精度浮点空数组(类型码是'd')
floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10**7)
fp.close()

print(floats2[-1])  # 0.8577432425578952
print(floats2 == floats)  # True

# ---------------------- 内存视图 memoryview -------------------
