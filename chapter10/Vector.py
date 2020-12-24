#-*- coding = utf-8 -*-
#@Time : 2020/12/11 9:04
#@Author : straightup
"""
兼容Vector2d的多维Vector
使用组合模式而不使用继承
"""
from array import array
import functools
import operator
import numbers
import reprlib
import math

class Vector:
    typecode = 'd'

    def __init__(self, components):
        """
        self._components是"受保护"的属性
        把Vector的分量保存在一个数组中
        """
        self._components = array(self.typecode, components)

    def __iter__(self):
        """为了迭代,使用self._components构建一个迭代器"""
        return iter(self._components)

    def __repr__(self):
        # 获取有限长度的表示形式 如 array('d', [0.0, 1.0, 2.0, ...])
        components = reprlib.repr(self._components)
        # 去掉前面的 array('d' 和后面的 ), 即只保留 [0.0, 1.0, 2.0, ...]
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    # def __eq__(self, other):
    #     return tuple(self) == tuple(other)

    # 提高大向量比较的效率
    # def __eq__(self, other):
    #     if len(self) != len(other):
    #         return False
    #     for a, b in zip(self, other):  # a, b分别为self和other的实例,只要有一个实例不同就返回False
    #         if a != b:
    #             return False
    #     return True

    # 再次升级
    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    # 散列
    def __hash__(self):
        hashes = (hash(x) for x in self._components)  # 生成器表达式
        return functools.reduce(operator.xor, hashes, 0)  # 0是初始值

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    # 实现可切片的序列
    def __len__(self):
        return len(self._components)

    # def __getitem__(self, index):
    #     return self._components[index]
    # 正确处理切片,返回实例对象
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    shortcut_names = 'xyzt'
    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)  # 查找那个字母的位置
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    # 不允许给单个小写字母的属性(分量)赋值
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = "readonly attributes {attr_name!r}"
            elif name.islower():
                error = "readonly attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)



