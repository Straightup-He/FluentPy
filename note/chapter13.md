# 正确重载运算符

## 运算符重载基础

+ 不能重载内置类型的运算符
+ 不能新建运算符, 只能重载现有的
+ 某些运算符不能重载 ( is, and, or 和 not)



## 重载向量加法运算符 +

### 一个生成器

```python
def __add__(self, other):
	pairs = itertools.zip_longest(self, other, fillvalue=0.0)
	return Vector(a, b for a, b in pairs)

# pairs 是一个生成器, 会生成(a,b)形式的元组, 其中 a, b 分别来自 self 和 other, 如果self和other长度不同, 使用 fillvalue 填充较短的那个可迭代对象
```

### a + b 背后的秘密

```python
1.如果 a 有 __add__ 方法, 而且返回值不是 NotImplemented, 调用 a.__add__(b), 然后返回结果
2.如果 a 没有 __add__ 方法, 或者调用 __add__ 方法返回 NotImplemented, 检查 b 有没有 __radd__ 方法, 如果有, 而且没有返回 NotImplemented, 调用 b.__radd__(a), 然后返回结果
3.如果 b 没有 __radd__ 方法, 或者调用 __radd__ 方法返回 NotImplemented, 则抛出 TypeError, 并在错误消息中指明 操作数类型不支持 !
```

```python
NotImplemented != NotImplementedError
前者是特殊的单例值, 并非异常!
```

### 简单实现 \__radd__

```python
def __add__(self, other):
    try:
    	pairs = itertools.zip_longest(self, other, fillvalue=0.0)
		return Vector(a, b for a, b in pairs)
    except TypeError:
        return NotImplemented

def __radd__(self, other):
    return self + other

# __radd__ 直接委托 __add__, 直接调用适当的运算符
# 捕获异常返回 NotImplemented, 让解释器尝试调用反向方法, 如果反向方法返回 NotImplemented, 那么Python就会抛出 TypeError, 并返回标准的错误信息!
```



## 重载标量乘法运算符 *

```python
v1 = Vector([1, 2, 3])
v1 * 10 = Vector([10.0, 20.0, 30.0])
# 计算标量积, 结果是一个新Vector实例, 各个分量都会乘以x
# 也叫元素级乘法
```

### 实现最简可用的 \__mul__ 和 \_\_rmul__

```python
def __mul__(self, scalar):
    return Vector(n * scalar for n in self)

def __rmul__(self, scalar):
    return self * scalar

# 但这个在提供不兼容的操作数时会出现问题
```

### 显示检查抽象类型 ( 白鹅类型的应用 )

```python
import numbers

class Vector:
    ...
    def __mul__(self, scalar):
        if isinstance(scalar, numbers.Real):
            return Vector(n * scalar for n in self)
        else:
            return NotImplemented
    
    def __rmul__(self, scalar):
        return self * scalar
    
# numbers.Real 抽象基类涵盖了我们所需的全部类型, 而且还支持以后声明为 numbers.Real 的真实子类或虚拟子类的数值类型!
```

上述重载 + 和 * 的技术同样适用于很多运算符 (见书 p316 - 317)



## 众多比较运算符

Python 解释器对众多比较运算符的处理与前文类似, 不过在两个方面有重大区别 :

+ 正向和反向使用的是同一系列方法, 只是把参数对调了
  + 如 ==, 正反都是调用 \__eq__, 参数对调
  + 如 >, 正向使用 \_\_gt\__, 反向使用 _\_lt__ 方法, 参数对调
+ 对 == 和 != 来说, 如果反向调用失败, python 会比较对象的 ID, 而不抛出 TypeError

### 改进 Veator 的 \__eq__ 方法

```python
# 原先
def __eq__(self, other):
    return (len(self) == len(other) and 
           all(a == b for a, b in zip(self, other)))

va = Vector([1.0, 2.0, 3.0])
t3 = (1, 2, 3)
va == t3
# 这个结果并不理想, 太不严谨了
# 应该对操作数做些类型检查, 如果是Vector实例, name使用 __eq__ 方法, 否则返回 NotImplemented 交给Python处理

# 改进版
def __eq__(self, other):
    if isinstance(other, Vector):
    	return (len(self) == len(other) and 
           	all(a == b for a, b in zip(self, other)))
    else:
        return NotImplemented
```



## 增量赋值运算符

```python
import itertools

from chapter11.bingo import BingoCage
from chapter11.tombola import Tombola


class AddableBingoCage(BingoCage):
    
    def __add__(self, other):
        if isinstance(other, Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented
        
    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other)
            except TypeError:
                self_cls = type(self).__name__
                msg = 'right operand in += must be {!r} or an iterable'
                raise TypeError(msg.format(self_cls))
        self.load(other_iterable)
        return self  # 增量赋值特殊方法必须返回self
    
# 总结:
# __add__ 调用 AddableBingoCage 构造方法构建一个新实例作为结果返回
# __iadd__ 把修改后的 self 作为结果返回

```

# 小结

+ 了解了 Python 对运算符重载施加的一些限制
  + 禁止重载内置类型的运算符
  + 只能重载现有的运算符, 有几个例外 ( is, and, or, not )
+ 如何重载一元运算符
+ 如何重载中缀运算符
  + 为了让操作数支持其他类型, 我们返回特殊单例值 **NotImplemented**, 让解释器尝试对调操作数, 然后调用运算符的**反向特殊方法**
+ 如果操作数类型不同, 我们要检测出不能处理的操作数, 两个方法
  + 1. 鸭子类型 : 直接尝试执行运算, 如果有问题, 捕获 Typeerror 异常
  + 2. 显式使用 isinstance 测试
  + 鸭子类型更灵活, 但显式测试更能预知结果. 但如果使用显式测试, 不能测试具体类, 而要测试 numbers.Real 抽象基类 !
+ 众多比较运算符
  + == 和 != 的后备机制 ( 从不抛出错误, 因为Python会比较对象的 id 来做最后一搏 )
+ 讨论了增量赋值运算符
  + Python 处理这种运算符的方式是把它们当做**常规的运算符加上赋值操作**, 如a += b 其实会被当做 a = a + b 来处理, 这样始终会生成新对象. 因此**可变和不可变类型都能用**.
  + 对可变对象来说, 可以实现**就地特殊方法**, 例如支持 += 的 \__iadd__ 方法, 然后修改左操作数的值
  + \+  比 += 严格, 对序列类型来说, + 通常要求两个操作数属于同一类型, 而 += 的右操作数往往可以是任何可迭代对象