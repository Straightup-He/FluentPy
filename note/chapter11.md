# 接口: 从协议到抽象基类

**抽象类表示接口**

Python 没有 interface 关键字, 而且除了抽象基类, 每个类都有接口 : 类实现或继承的公开属性(方法或数据属性), 包括特殊方法(双下方法).

接口的补充定义 : 对象公开方法的子集, 让对象在系统中扮演特定的角色

## Python 喜欢序列

```
鉴于序列协议的重要性, 如果没有 __iter__ 和 __contains__ 方法, Python会调用 __getitem__ 方法, 设法让迭代和 in 运算符可用!
```

## 标准库中的抽象基类

+ collections.abc 模块提供了16个抽象基类
+ numbers 包

## 检查对象是否可调用 / 可哈希

```
isinstance(my_obj, Callable)  / callable(my_obj)
isinstance(my_obj, Hashable)
```

# 定义自己的抽象基类

```python
"""
从有限的集合中随机挑选物品,选出的物品没有重复,直到选完为止
Tombola抽象基类有四个方法, 其中两个是抽象方法(子类必须实现)
.load(...)  把元素放入容器
.pick(...)  从容器随机拿出一个元素, 返回选中的元素

.loaded(...)  如果容器至少有一个元素, 返回True
.inspect(...)  返回一个有序元组, 由容器中的现有元素构成, 不会修改容器的内容
"""
import abc

class Tombola(abc.ABC):
    
    @abc.abstractmethod
    def load(self, iterable):
        """从可迭代对象中添加元素"""
    
    @abc.abstractmethod
    def pick(self):
        """随机删除元素, 然后将其返回
        如果实例为空, 这个方法应该抛出`LookupError`
        """
    
    def loaded(self):
        """如果至少有一个元素, 返回 `True`, 否则返回 `False`"""
        return bool(self.inspect())
    
    def inspect(self):
        """返回一个有序元组, 由当前元素构成"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))
```

```python
涉及到的知识点:
1.自己定义的抽象基类必须继承 abc.ABC
2.抽象方法使用 @abc.abstractmethod 装饰器标记; 若是抽象类方法按下面写法:
	@classmethod
	@abc.abstractmethod
	def func()...
3.抽象基类的子类必须要实现抽象方法
4.声明抽象基类的最简单方法是继承 abc.ABC 或其他抽象基类
```



## 虚拟子类

```
1.白鹅类型, 即便不继承, 也有办法把一个类注册为抽象基类的虚拟子类
2.注册虚拟子类的方式是在抽象基类上调用register方法, 但是注册的类不会从抽象基类中继承任何方法和属性
3.为了避免运行错误, 虚拟子类要实现所需的全部方法
```

```python
#-*- coding = utf-8 -*-
#@Time : 2020/12/14 22:54
#@Author : straightup
"""
Tombola的虚拟子类
"""
from random import randrange
from tombola import Tombola

@Tombola.register
class Tombolist(list):

    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty Tombolist')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))
    
# 实例化
t = Tombolist()

print(isinstance(t, Tombola))  # True
print(issubclass(Tombolist, Tombola))  # True 说明是Tombola的子类

print(Tombolist.__mro__)
# (<class '__main__.Tombolist'>, <class 'list'>, <class 'object'>)
# 只列出"真实的"超类, 因此 Tombolist 没有从 Tombola 中继承任何东西
```

# 小结

+ 非正式接口 (协议)
+ Python 对序列协议十分支持, 一个类只要实现了 \__getitem__ 方法, 那么 python 会设法迭代它, 而且 in 运算符也能用了 !
+ 白鹅类型 : 可以使用抽象基类明确声明接口, 而且类可以子类化抽象基类 (继承) 或使用抽象基类注册, 来宣称它实现了某个接口
+ 显示继承抽象基类的优缺点:
  + 优点: 继承大量方法, 可以直接使用
  + 缺点: 要实现必须实现但用不上的方法
+ 介绍了 abc.ABC 和 numbers 中的抽象基类
+ 自己创建了抽象基类, 并实现了其子类和虚拟子类