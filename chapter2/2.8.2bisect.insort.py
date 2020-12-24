#-*- coding = utf-8 -*-
#@Time : 2020/12/1 23:20
#@Author : straightup

import bisect
import random

SIZE = 7

random.seed(1792)

my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    bisect.insort(my_list, new_item)
    print('%2d  ->' % new_item, my_list)
"""
11  -> [11]
 7  -> [7, 11]
 6  -> [6, 7, 11]
 5  -> [5, 6, 7, 11]
 7  -> [5, 6, 7, 7, 11]
 5  -> [5, 5, 6, 7, 7, 11]
10  -> [5, 5, 6, 7, 7, 10, 11]
"""
