#-*- coding = utf-8 -*-
#@Time : 2020/12/8 22:21
#@Author : straightup
"""
标识, 相等性和别名
"""
charles = {'name': 'Charles L. Dodgson', 'born': 1832}
lewis = charles
print(lewis is charles)  # True

# 这时有个假冒者
alex = {'name': 'Charles L. Dodgson', 'born': 1832}
print(alex == charles)  # True
print(alex is charles)  # False

# 浅复制
'''
l1 = [3, [66, 55], (7, 8)]
l2 = list(l1)
l1[1].remove(55)
print(l1)  # [3, [66], (7, 8)]
print(l2)  # [3, [66], (7, 8)]
l2[1] += [22, 33]
l2[2] += (10, 11)
print(l1)  # [3, [66, 22, 33], (7, 8)]
print(l2)  # [3, [66, 22, 33], (7, 8, 10, 11)]
'''

