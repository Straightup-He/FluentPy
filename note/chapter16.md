# 协程

**协程文档是最匮乏, 最鲜为人知的Python特性**

to yield : 产出 / 让步

+ 产出一个值提供给next()的调用方
+ 做出让步, 暂停执行生成器，让调用方继续工作，直到需要另一个值再调用next()

**协程**与生成器类似，都是定义体中包含yield关键字的函数。但在协程中，yield通常出现在表达式的右边，可以产出值也可以不产出。协程可能会**从调用方接收数据**，不过调用方把数据提供给协程使用的是 .send(data) 方法，而不是 next()。

yield 关键字甚至可以不接收和传出数据，不管数据如何流动，yield都是一种**流程控制工具**，使用它可以实现协作式多任务：协程可以把控制器让步给中心调度程序，从而激活其他的协程。

==从根本上把yield视作控制流程的方式！==

# 生成器如何进化成协程？

**协程是指一个过程，这个过程与调用方协作，产出由调用方提供的值**

+ .send(...)		发送数据（会成为yield表达式的值）
+ .throw(...)      让调用方抛出异常，在生成器中处理
+ .close(...)        终止生成器

# 用作协程的生成器的基本行为

简单的协程行为展示：

```python
def simple_coroutine():
    print('-> coroutine started')
    x = yield
    print('-> coroutine received:', x)

my_coro = simple_coroutine()
print(my_coro)  # <generator object simple_coroutine at 0x0000012AD1A7BE58>

# 因为生成器还没启动，需要调用next()，让生成器在yield语句暂停
next(my_coro)
my_coro.send(42)
"""
-> coroutine started

-> coroutine received: 42
Traceback (most recent call last):
  File "C:/Users/harris/Desktop/fluentPy/chapter16/16.1协程展示.py", line 14, in <module>
    my_coro.send(42)
StopIteration
"""
```

==send方法的值会成为暂停的yield表达式的值==，所以仅当协程处于暂停状态时才能调用send方法。如果协程未激活（调用next），就立即把None以外的值发给它则会报错：""" TypeError: can't send non-None value to a just-started generator """

## 协程可以处在四个状态

> inspect.getgeneratorstate 可以查看

+ ' GEN_CREATED '：等待开始执行
+ ' GEN_RUNNING '：解释器正在执行
+ ' GEN_SUSPENDED '：在yield表达式暂停
+ ' GEN_CLOSED '：执行结束

产出两个值的协程：

```python
def simple_coro2(a):
    print('-> started: a =', a)
    b = yield a
    print('-> received: b =', b)
    c = yield a+b
    print('-> received: c =', c)

my_coro2 = simple_coro2(14)

from inspect import getgeneratorstate
print(getgeneratorstate(my_coro2))  # GEN_CREATED

next(my_coro2)
"""
-> started: a = 14
14
"""

print(getgeneratorstate(my_coro2))  # GEN_SUSPENDED

print(my_coro2.send(28))
"""
-> received: b = 28
42
"""
print(my_coro2.send(99))
"""
-> received: c = 99
Traceback (most recent call last):
  File "C:/Users/harris/Desktop/fluentPy/chapter16/16.2产出两个值的协程.py", line 23, in <module>
    my_coro2.send(99)
StopIteration
"""
print(getgeneratorstate(my_coro2))  # GEN_CLOSED
```

执行过程：

+ 首先 next() 先激活协程，执行到第一句 yield 语句，记住赋值语句的代码==先执行等号右边==，也就是 b = yield a，所以产出 a 。产出a后在 yield 语句暂停，等待为 b 赋值
+ .send(x)方法传入的参数发送给暂停的协程，yield 表达式就等于该参数的值，所以 b 的值则为传入的参数的值
+ 之后执行语句到第二句 yield 语句，c = yield a+b，产出 a+b 的值，并等待为 c 赋值
+ 最后.send(y) 方法再传入一个值，赋值给c，后面没有 yield 语句了，导致生成器对象抛出 StopIteration 异常

# 使用协程计算移动平均值

```python
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count
```

while True 这个无限循环表明：

+ 只要调用方不断把值发送给这个协程，它就会一直接收值，然后产出结果
+ 仅当调用方在协程上使用 .close() 方法，或者没有对协程的引用而被垃圾回收时，这个协程才终止

使用协程的好处：total 和 count 声明为局部变量即可，无需使用实例属性或闭包在多次调用之间保持上下文

测试：

```python
coro_avg = averager()
# 首先激活协程
next(coro_avg)

print(coro_avg.send(10))  # 10.0
print(coro_avg.send(30))  # 20.0
print(coro_avg.send(5))   # 15.0
```

# 预激协程的装饰器

**如果不预激，那么协程没什么用，但用next激活又很麻烦**

装饰器代码：

```python
from functools import wraps

def coroutine(func):
    """装饰器：向前执行到第一个`yield`表达式，预激`func`"""
    @wraps(func)  
    def primer(*args, **kwargs):  #1
        gen = func(*args,**kwargs)  #2
        next(gen)  #3
        return gen #4
    return primer
"""
1.把被装饰的func替换成primer函数；返回的是预激后的生成器
2.调用被装饰的func，获取生成器对象
3.预激生成器
4.返回生成器
"""
```

@coroutine装饰器用法：

```python
@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count

# 测试计算移动平均值的协程
coro_avg = averager()
from inspect import getgeneratorstate
print(getgeneratorstate(coro_avg))
# GEN_SUSPENDED（不用手动next激活，已经进入暂停状态！）

print(coro_avg.send(10))
print(coro_avg.send(30))
print(coro_avg.send(5))
"""
10.0
20.0
15.0
"""
```

# 终止协程和异常处理

**协程中未处理的异常会向上冒泡，传给next函数或send方法的调用方**

协程内部没有处理异常的话，遇到异常会终止，需要重新激活！否则抛出 StopIteration 异常！

==暗示了终止协程的一种方法==：发送某个哨符值，让协程退出。内置的 None 和 Ellipsis 等常量经常用作哨符值。

py2.5开始，可以在生成器对象上调用 **throw** 和 **close** 方法，显示地把异常发给协程：

+ throw(exc_type[, exc_value[, traceback]])：致使生成器在暂停的 yield 表达式处抛出指定的异常。<u>如果生成器处理了异常，则代码会前进执行下一个 yield表达式，产出的值会成为调用 throw 方法得到的返回值。</u>若无处理，则向上冒泡。
+ close()：致使生成器在暂停的 yield 表达式处抛出 GeneratorExit 异常。若生成器没有处理这个异常，或者抛出了 StopIteration 异常（通常是指运行到结尾），调用方不会报错。<u>如果收到 GeneratorExit 异常，生成器一定不能产出值</u>，否则解释器会抛出 RuntimeError 异常！生成器抛出的其他异常则向上冒泡，传给调用方。

## 举例说明：

学习在协程中处理异常的测试代码：

```python
class DemoException(Exception):
    """为这次演示定义的异常类型。"""

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> coroutine received: {!r}'.format(x))
    raise RuntimeError('This line should never run.')

# 最后一行：This code is unreachable（永远不会执行...）因为只有未处理的异常才会终止那个无限循环，而一旦出现未处理的异常，协程亦随之终止。
```

测试：

```python
# -------- 激活和关闭 demo_exc_handling，没有异常 -----------
exc_coro = demo_exc_handling()
next(exc_coro)  # -> coroutine started
exc_coro.send(11)  # -> coroutine received: 11
exc_coro.send(22)  # -> coroutine received: 22

exc_coro.close()
from inspect import getgeneratorstate
print(getgeneratorstate(exc_coro))  # GEN_CLOSED
```

```python
# 把 DemoException 异常传入 demo_exc_handling 不会导致协程终止
exc_coro = demo_exc_handling()
next(exc_coro)  # -> coroutine started
exc_coro.send(11)  # -> coroutine received: 11
exc_coro.throw(DemoException)
"""
*** DemoException handled. Continuing...
"""
from inspect import getgeneratorstate
print(getgeneratorstate(exc_coro))  # GEN_SUSPENDED
```

```python
# 如果传入协程的异常没有处理，会导致协程终止！
exc_coro = demo_exc_handling()
next(exc_coro)  # -> coroutine started
exc_coro.send(11)  # -> coroutine received: 11
exc_coro.throw(ZeroDivisionError)  # 报错！
"""
Traceback (most recent call last):
    ...
ZeroDivisionError
"""
from inspect import getgeneratorstate
print(getgeneratorstate(exc_coro))  # GEN_CLOSED
```

如果不管协程如何结束都想做些清理工作，要把协程定义体中的相关代码放入 try-finally 块中：

```python
class DemoException(Exception):
    """为这次演示定义的异常类型。"""

def demo_finally():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> coroutine received: {!r}'.format(x))
        finally:
            print('-> coroutine ending...')
```

# 让协程返回值

计算平均移动值（返回累计值，而不是每次都产出）

```python
from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)

# 测试
coro_avg = averager()
next(coro_avg)
coro_avg.send(10)
coro_avg.send(30)
coro_avg.send(6.5)
"""
# 普通版，返回值在异常中显示
coro_avg.send(None)

Traceback (most recent call last):
  ...
StopIteration: Result(count=3, average=15.5)
"""
# 捕获异常版
try:
    coro_avg.send(None)
except StopIteration as exc:
    result = exc.value
print(result)   # Result(count=3, average=15.5)
```

# 使用 yield from

yield from 可用于简化 for 循环中的 yield 表达式

```python
def gen():
    for c in 'AB':
        yield c
    for i in range(1, 3):
        yield i
# 等价于
def gen():
    yield from 'AB'
    yield from range(1, 3)

# 还能这样
def chain(*iterables):
    for it in iterables:
        yield from it
s = 'ABC'
t = tuple(range(3))
list(chain(s, t))  # --> ['A', 'B', 'C', 0, 1, 2]
```

**yield from x 表达式对 x 对象做的第一件事：调用 iter(x) 获取迭代器。因此，x 可以是任何可迭代对象！**

**yield from** 的主要功能是打开**双向通道**，把==最外层的调用方法==与==最内层的子生成器==连接起来，这样二者可以直接发送和产出值，还可以直接传入异常，而不用在位于中间的协程中添加处理异常的代码！

**yield from 结构的几个专业术语：**

+ 委派生成器：包含 yield from <iterable> 表达式的生成器函数
+ 子生成器：从 yield from <iterable> 表达式获取的生成器
+ 调用方：调用委派生成器的客户端代码（委派生成器也是调用方，它调用了子生成器）

使用 yield from 计算平均值并输出统计报告：

```python
from collections import namedtuple

Result = namedtuple('Result', 'count average')

# 子生成器
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)

# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from averager()

#客户端代码，即调用方
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)
    print(results)
    report(results)

# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit
        ))

data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.3, 41.7],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.3, 41.4],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48],
}

if __name__ == '__main__':
    main(data)
"""
{'girls;kg': Result(count=6, average=42.15), 'girls;m': Result(count=6, average=1.4349999999999998), 'boys;kg': Result(count=6, average=41.41666666666667), 'boys;m': Result(count=6, average=1.3833333333333335)}
 6 boys  averaging 41.42kg
 6 boys  averaging 1.38m
 6 girls averaging 42.15kg
 6 girls averaging 1.43m
"""
```



























