#-*- coding = utf-8 -*-
#@Time : 2020/12/1 8:16
#@Author : straightup
'''
一个简单的二维向量类
'''
from math import hypot

class Vector(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        """
        字符串表示形式, 控制打印实例变量的样式
        :return:
        """
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        """
        将模的值作为判断的标准,为 0 则返回 false
        :return:
        """
        # return bool(abs(self))
        return bool(self.x or self.y)

    def __add__(self, other):
        """
        加法操作
        :param other: 另一个向量
        :return:返回新创建的向量对象
        """
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


v1 = Vector(3, 4)
print(abs(v1))   # 5.0
print(v1)    # Vector(3, 4)
print(bool(v1))  # True

v2 = Vector(2, 1)
print(v1 + v2)  # Vector(5, 5)










