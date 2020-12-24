#-*- coding = utf-8 -*-
#@Time : 2020/12/3 7:32
#@Author : straightup
"""
高阶函数
"""
# 根据单词长度排序
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
print(sorted(fruits, key=len))
# ['fig', 'apple', 'cherry', 'banana', 'raspberry', 'strawberry']
print(sorted(fruits, key=len, reverse=True))
# ['strawberry', 'raspberry', 'cherry', 'banana', 'apple', 'fig']

# 根据反向拼写给单词列表排序(创建押韵词典,berry的都聚在一起了!)
def my_reverse(word):
    return word[::-1]

print(my_reverse('test'))   # tset
print(sorted(fruits, key=my_reverse))
# ['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
