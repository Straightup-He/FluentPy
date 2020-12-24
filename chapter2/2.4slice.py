#-*- coding = utf-8 -*-
#@Time : 2020/12/1 15:26
#@Author : straightup
"""
切片
"""
text = "kjlajdownccs,lqm"
block = slice(2, 5)
print(text[2:5])    # laj
print(text[block])  # laj

l = [1, 2, 3]
print(l*2)  # [1, 2, 3, 1, 2, 3]
print(l)  # [1, 2, 3]

# +=的谜题
t = (1, 2, [30, 40])
t[2] += [50, 60]
# print(t)


