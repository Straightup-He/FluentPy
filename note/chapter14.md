# 可迭代的对象、迭代器和生成器

**迭代是数据处理的基石**

Python语言内部，迭代器用于支持：

+ for循环
+ 构建和扩展集合类型
+ 逐行遍历文本文件
+ 列表推导、字典推导和集合推导
+ 元组拆包
+ 调用函数时，使用*拆包实参

## Sentence类第一版：单词序列

```python
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        """用于生成大型数据结构的简略字符串表示形式
        reprlib.repr默认生成30个字符"""
        return 'Sentence(%s)' % reprlib.repr(self.text)


# 测试Sentence实例可否迭代
s = Sentence('"The time has come," the Walrus said,')
print(s)  # Sentence('"The time ha... Walrus said,')

for word in s:
    print(word)
"""
The
time
has
come
the
Walrus
said
"""
print(list(s))  # ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']
```

## 序列可迭代的原因：iter函数

解释器需要迭代对象 x 时，会自动调用 iter(x)

任何Python序列都可迭代的根本原因：都实现了\__getitem__ 方法！（其实标准的序列也都实现了\_\_iter__ 方法）

不同设计类型对对象是否可迭代的定义：

+ 鸭子类型：不仅要实现`__iter__`方法，还要实现`__getitem__`（参数为从0开始的整数）
+ 白鹅类型：如果实现`__iter__`方法，就认为对象可迭代

```python
# 上面定义的Sentence类是可迭代的，但无法通过测试！
print(isinstance(s, abc.Iterable))  # False
print(issubclass(Sentence, abc.Iterable))  # False

# 从Python3.4开始，检查对象x能否迭代，最准确的方法是：调用iter(x)函数
print(iter(s))  # <iterator object at 0x0000000002581278>

# 这比使用 isinstance(x, abc.Iterable) 更准确，因为 iter(x)函数会考虑到遗留的 __getitem__ 方法，而 abc.Iterable 类则不考虑。
```

## 可迭代的对象与迭代器的对比

需要明确的关系：Python 从可迭代的对象中获取迭代器 (迭代器 = iter(可迭代对象))

StopIteration 异常表明迭代器到头了，Python内部会进行处理。

### 标准的迭代器接口有两个方法

`__next__` ：返回下一个可用元素，如果没有元素，抛出 StopIteration 

`__iter__` ：返回 self，以便在应该使用可迭代对象的地方使用迭代器，例如 在 for 循环中

检查对象 x 是否为**迭代器**最好的方式是调用 isinstance(x, abc.Iterator)

### 定义

**可迭代的对象：** 使用 iter 内置函数可以获取迭代器的对象。如果对象实现了能返 回迭代器的 `__iter__` 方法，那么对象就是可迭代的。序列都可以迭代；实现了 `__getitem__` 方法，而且其参数是从零开始的索引，这种对象也可以迭代。

**迭代器：** 迭代器是这样的对象：实现了无参数的 `__next__` 方法，返回序列中的下一个元素；如果没有元素了，那么抛出 StopIteration 异常。Python 中的迭代器还实现了 `__iter__` 方法，因此迭代器也可以迭代。因为内置的 iter(...) 函数会对**序列**做特殊处理，所以第 1 版 Sentence 类可以迭代（但不标准）。

## Sentence类第二版：典型的迭代器

```python
"""
Sentence类第二版：典型的迭代器
"""
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        """返回一个迭代器"""
        return SentenceIterator(self.words)


class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0
        
    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return word
    
    def __iter__(self):
        return self

```

### 注意：

不要混淆可迭代对象和迭代器，可迭代对象有个 `__iter__`方法，每次都实例化一个新的迭代器。而迭代器要实现 `__next__ `方法，返回单个元素，此外还要实现`__iter__`方法，返回迭代器本身。

因此，迭代器可以迭代，但可迭代对象不是迭代器！

## Sentence类第三版：生成器函数

更符合Python习惯的方式

```python
"""
Sentence类第三版：生成器函数
"""
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word
# 完成！
# 不管有没有 return 语句，生成器函数都不会抛出 StopIteration 异常，而是在生成完全部值之后会直接退出
# 不用再单独定义一个迭代器类！
```

### 生成器函数的工作原理

**只要 Python 函数的定义体中有 yield 关键字，该函数就是生成器函数。调用生成器函数时，会返回一个生成器对象**

```python
def gen():
    yield 1
    yield 2
gen   -->  <function gen_123 at 0x...>   #函数对象
gen() -->  <generator object gen_123 at 0x...>  #生成器对象

for i in gen():
    print(i)
"""
1
2
"""

g = gen()
print(next(g))	# 1
print(next(g))	# 2
print(next(g))	# 抛出 StopIteration 异常
```

迭代时，for 机制的作用与 g = iter(gen_AB()) 一样，用于**获取生成器对象**，然后每次迭代时调用 next(g)

```python
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end')

for item in gen_AB():
    print('>>>', item)
"""
start
>>> A
continue
>>> B
end
"""
# 注意！每次循环结束会在yield停住！下一次循环从上次结束的地方开始！
# 到达生成器函数定义体的末尾时，生成器对象抛出 StopIteration 异常。for 机制会捕获异常，因此循环终止时没有报错。

```

## Sentence类第四版：惰性实现

前面几例 `__init__` 方法急迫地构建好了文本中的单词列表，然后将其绑定到 self.words 属性上，这样就要处理整个文本！

re.finditer 函数是 re.findall 的惰性版本，返回的不是列表而是一个**生成器**

```python
"""
Sentence类第四版：惰性函数
"""
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()
        
# 不再需要words列表
```

## Sentence类第五版：生成器表达式

生成器表达式可以理解为列表推导的惰性版本：不会迫切地构建列表，而是返回一个生成器，按需惰性生成元素。

```python
"""
Sentence类第五版：生成器表达式
"""
import re
import reprlib


RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))
    
# 与第四版的差别：__iter__方法用生成器表达式取代生成器函数
# 效果一样：通过调用 __iter__方法得到一个生成器对象
```

### tip

如果函数或构造方法只有一个参数，传入生成器表达式时不用写一对调用函数的括号，再写一对括号围住生成器表达式，只写一对括号就行了

```python
def __mul__(self, scalar):
	if isinstance(scalar, numbers.Real):
		return Vector(n * scalar for n in self) ##
else:
	return NotImplemented
```

## 等差数列生成器

探讨如何生成不同数字类型的有穷等差数列

+ ArithmeticProgression 类

```python
class ArithmeticProgression:

    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end  # None -> 无穷数列

    def __iter__(self):
        # 行把 self.begin 赋值给 result，不过会先强制转换成前面的加法算式得到的类型
        result = type(self.begin + self.step)(self.begin)
        forever = self.end is None  # bool
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index
```

+ aritprog_gen 生成器函数（有穷等差数列**函数版**）

```python
def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index
```

+ 使用itertools模块生成等差数列

```python
"""
itertools.count 函数返回的生成器能生成多个数。如果不传
入参数，则会生成从零开始的整数数列
"""
import itertools
gen = itertools.count(1, .5)
next(gen)
1
next(gen)
1.5
next(gen)
2.0

# 然而，itertools.count 函数从不停止！
```

```python
"""
itertools.takewhile 函数则不同，它会生成一个使用另一个
生成器的生成器，在指定的条件计算结果为 False 时停止
"""
gen = itertools.takewhile(lambda n:n<3, itertools.count(1, .5))
list(gen)
[1, 1.5, 2.0, 2.5]
```

+ 完整版

```python
import itertools

def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen

"""
注意：aritprog_gen 不是生成器函数，因为定义体中没有 yield 关键字。但是它会返回一个生成器，因此它与其他生成器函数一样，也是生成器工厂函数！
"""
```

## 现有的标准库中的生成器函数

**避免反复造轮子**

+ 用于**过滤**的生成器函数：从输入的可迭代对象中产出元素的子集，而且不修改元素本身。

+ 用于**映射**的生成器函数：在输入的单个可迭代对象（map 和 starmap 函数处理多个可迭代的对象）中的各个元素上做计算，然后返回结果。

  ```python
  # 从 1! 到 10!，计算各个数的阶乘
  sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
  
  list(itertools.accumulate(range(1, 11), operator.mul))
  [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800] 
  ```

+ 用于**合并**的生成器函数，这些函数都从输入的多个可迭代对象中产出元素

  + itertools.zip_longest 函数的作用与 zip 类似，不过输入的所有可迭代对象都会处理到头，如果需要会填充 None

    ```python
    >>> list(zip('ABC', range(5), [10, 20, 30, 40])) 
    [('A', 0, 10), ('B', 1, 20), ('C', 2, 30)]
    
    >>> list(itertools.zip_longest('ABC', range(5)))
    [('A', 0), ('B', 1), ('C', 2), (None, 3), (None, 4)]
    
    # fillvalue 关键字参数用于指定填充的值
    >>> list(itertools.zip_longest('ABC', range(5), fillvalue='?'))
    [('A', 0), ('B', 1), ('C', 2), ('?', 3), ('?', 4)]
    ```

  + itertools.product 生成器是计算笛卡儿积的惰性方式

    ```python
    >>> list(itertools.product('ABC', range(2)))
    [('A', 0), ('A', 1), ('B', 0), ('B', 1), ('C', 0), ('C', 1)]
    ```

+ 把输入的各个元素**扩展**成多个**输出**元素的生成器函数

+ 用于产出输入的可迭代对象中的全部元素，不过会以某种方式重新排列

  + ```python
    # itertools.groupby 函数分组
    
    list(itertools.groupby('LLLLAALLGGG'))
    [('L', <itertools._grouper object at 0x0000000003610CC0>), ('A', <itertools._grouper object at 0x0000000003610BA8>), ('L', <itertools._grouper object at 0x0000000003610C18>), ('G', <itertools._grouper object at 0x0000000003610FD0>)]
    for char, group in itertools.groupby('LLLLAAALLGG'):
    ...     print(char, '->', list(group))
    ...     
    L -> ['L', 'L', 'L', 'L']
    A -> ['A', 'A', 'A']
    L -> ['L', 'L']
    G -> ['G', 'G']
    ```

## yield from：不同的生成器结合在一起使用

**如果生成器函数需要产出另一个生成器生成的值，传统的解决方法是使用嵌套的 for 循环**

```python
# def chain(*iterables):
#     for it in iterables:
#         for i in it:
#             yield i

def chain(*iterables):
    for i in iterables:
        yield from i

s = 'ABC'
t = tuple(range(3))
print(list(chain(s, t)))  # ['A', 'B', 'C', 0, 1, 2]

# yield from i 完全代替了内层的 for 循环
```

除了代替循环之外，yield from 还会创建通道，把内层生成器直接与外层生成器的客户端联系起来。把生成器当成协程使用时，这个通道特别重要，不仅能为客户端代码生成值，还能使用客户端代码提供的值。

## 可迭代的归约函数

**接受一个可迭代的对象，然后返回单个结果**

+ all / any
+ max / min
+ functools.reduce
+ sum

还有一个内置的函数接受一个可迭代的对象，返回**不同**的值——sorted

## 深入分析iter函数

在 Python 中迭代对象 x 时会调用 iter(x)

iter 函数还有一个鲜为人知的用法：传入两个参数，使用常规的函数或任何可调用的对象创建迭代器！

```python
"""
使用 iter 函数掷骰子，直到掷出 1 点为止
"""
from random import randint

def d6():
    return randint(1, 6)

d6_iter = iter(d6, 1)
print(d6_iter)  # <callable_iterator object at 0x0000000002169198>

for roll in d6_iter:
    print(roll)
"""
3
6
4
因为 1 是哨符，肯定不会打印 1，
"""
```

### 案例分析：在数据库转换工具中使用生成器

+ 略

## 把生成器当成协程

```python
.send()方法和.__next()方法一样,能使生成器前进到下一个 yield 语句
但是.send()方法允许客户代码和生成器之间双向交换数据, 而.__next()方法只允许客户从生成器中获取数据
```

# 小结

+ 可迭代对象和迭代器, 生成器
+ 本章编写了几个类, 用于读取可能内容很多的文件, 并迭代里面的单词. 但因为用了生成器, 所以在重构的过程中, 代码逐渐简短易读, 并学习了生成器的原理
+ 编写了生成等差数列的生成器
+ itertools 模块
+ 标准库的24个通用生成器函数
+ 内置 iter 函数 : 首先以 iter(x) 的形式调用时返回的是迭代器; 之后分析, 以 iter(func, sentinel) 形式调用时, 能使用任何函数构建迭代器
+ 数据库转换工具实例 (没看)
+ yield from 句法, 协程 (简单介绍, 之后会详细讲解)

