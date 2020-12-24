#-*- coding = utf-8 -*-
#@Time : 2020/12/1 11:48
#@Author : straightup

# 列表推导式
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for size in sizes
                        for color in colors]
# print(tshirts)
# [('black', 'S'), ('white', 'S'), ('black', 'M'), ('white', 'M'), ('black', 'L'), ('white', 'L')]

# 生成器表达式
for tshirt in ('%s %s' % (color, size) for color in colors
                                        for size in sizes):
    print(tshirt)
"""
black S
black M
black L
white S
white M
white L
"""