# 序列的修改, 散列和切片

拓展 : gensim 包使用 Numpy 和 SciPy 实现了用于处理自然语言和检索信息的向量空间模型



## 序列协议

**只需实现 \_\_len__ 和 \_\_getitem__ 方法**

实现了序列协议, 无论它继承的是不是序列类型的类, 它都是序列

协议是非正式的, 没有强制力, 通常根据使用场景只需要实现一个协议的部分即可 (如为了支持迭代只需实现 \_\_getitem__)



## 切片原理

**indices** 属性(方法)

用于优雅地处理缺失索引和负数索引, 以及长度超过目标序列的切片. 这个方法会整顿元祖, 把 start, stop, step 都变成非负数, 且都落在指定长度序列的边界内



## 动态存取属性

查找实例对象是否有某个属性, 会先去实例里找, 如果没有就去其父类中找, 如果都没有, 则会调用实例中定义的 \__getattr__ 方法, 传入 self 和 属性名称的字符串形式 (如 'x')



## 再次提到 operator 模块

```python
"""
计算整数0~5的累积异或的3种方式
"""
n = 0
for i in range(1, 6):
    n ^= i
print(n)

import functools
res = functools.reduce(lambda a, b: a ^ b, range(6))
print(res)

import operator
res = functools.reduce(operator.xor, range(6))
print(res)

# 使用reduce函数最好能提供第三个参数(初始值)
# + | ^		初始值应该是0
# * &		初始值应该是1
```

# 小结

+ Vector 的行为之所以像序列, 是因为它实现了 \__getitem__ 和 \_\_len__ 方法
+ 协议, 是鸭子类型语言使用的非正式接口
+ 切片背后的工作原理 : 创建 slice(a,b, c) 对象, 交给 \__getitem__ 处理
+ 通过 \__getattr__ 方法实现 my_vec.x 这样的表示法(只读), 通过 \_\_setattr__ 方法实现 my_vec.x = 7 这样的赋值方法. 大多数情况下这两个方法要一起实现, 避免行为不一致
+  实现 \__hash__ 方法特别适合用 functools.reduce 函数
+ operator 模块 xor() 异或