# 函数装饰器和闭包

## 装饰器基础知识

```
装饰器是可调用的对象,其参数是另一个函数(被装饰的函数)
装饰器可能会处理被装饰的函数,然后把它返回.或者将其替换成另一个函数或可调用对象

函数装饰器在导入模块时立即执行!

装饰器通常在一个模块中定义,然后再其他模块应用
装饰器在内部定义一个函数,然后将其返回
```

## 用装饰器改进"策略"模式

```python
"""
装饰器改进"策略"模式
"""
promos = []

def promotion(promo_func):
    """被promotion装饰的函数都会添加到promos列表中"""
    promos.append(promo_func)
    return promo_func

@promotion
def fidelity_promo(order):
    """为积分为1000及以上的顾客提供 5%的折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

@promotion
def bulk_item_promo(order):
    """单个商品数量为20个或以上时提供 10%的折扣"""
    discount_money = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount_money += item.total() * .1
    return discount_money

@promotion
def large_order_promo(order):
    """订单中的不同商品达到 10个或以上时提供 7%折扣"""
    distinct_items = {item.product for item in order.cart}
    return order.total() * .07 if len(distinct_items) >= 10 else 0

def best_promo(order):
    """选用最佳策略"""
    return max(promo(order) for promo in promos)

# 被@promotion装饰的函数都会添加到promos列表中!
# @promotion装饰器突出了被装饰函数的作用,还便于临时禁用某个促销策略:只需把装饰器注释掉
```

## 变量作用规则

```python
b = 6
def f1(a):
    print(a)
    print(b)
    b = 9
f(3)
# a成功打印,b打印错误!
# 原因:python编译函数的定义体时,判断b是局部变量,因为在函数体内给b赋值了

# 解决:声明全局变量
b = 6
def f1(a):
    global b
    print(a)
    print(b)
    b = 9
f(3)
```

## 闭包

+ 只有涉及嵌套函数才有闭包问题

```python
# ------------------------ 函数式实现 -------------------------
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager

# 每次调用 make_averager 都会返回一个 averager 函数对象,再加括号即可执行!
avg = make_averager()
print(avg(10))      # 10.0
print(avg(11))      # 10.5
print(avg(12))      # 11.0

print(avg.__code__.co_varnames)  # ('new_value', 'total')  局部变量
print(avg.__code__.co_freevars)  # ('series',)  自由变量

# 数据保存在这!
print(avg.__closure__)  # (<cell at 0x000001DF996228E8: list object at 0x000001DF99576248>,)
print(avg.__closure__[0].cell_contents)  # [10, 11, 12]

# averager 的闭包延伸到函数的作用域外,包含自由变量 series 的绑定!
# __code__.co_varnames	查看局部变量
# __code__.co_freevars	查看自由变量
# 自由变量的绑定在返回函数的 __closure__ 属性中,对应于 __code__.co_freevars 中的一个名称,而数据存在其 cell_contents 属性
```

+ 在内嵌函数体中对 "自由变量" 赋值的话它就不自由了, 这样会隐式创建局部变量
+ 如果只是调用则不会出现问题

### 改进版, 不保存所有历史的版本

```python
# 不保存所有历史的版本
# 自由变量为不可变类型,+=会进行赋值,所以要nonlocal声明非局部变量
def make_averager():
    count = 0
    total = 0
    
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += 1
        total += new_value
        return total/count
    return averager
```



## 实现一个简单的装饰器

```python
"""
一个简单的装饰器,输出函数的运行时间
"""
import time

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
```

### 测试装饰器

```python
import time
from clockdeco import clock

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

if __name__ == '__main__':
    print('*'*40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))

"""
**************************************** Calling snooze(.123)
[0.13334950s] snooze(0.123) -> None
**************************************** Calling factorial(6)
[0.00000280s] factorial(1) -> 1
[0.00006780s] factorial(2) -> 2
[0.00011840s] factorial(3) -> 6
[0.00016270s] factorial(4) -> 24
[0.00020720s] factorial(5) -> 120
[0.00025660s] factorial(6) -> 720
6! = 720
"""
```

```python
# 工作原理
@clock							def fact(n):
def fact(n):	-- 等价于 -->	    	pass
    pass						fact = clock(fact) = clocked

# 所以 fact 保存的是 clocked 函数的引用,之后每次调用 fact(n) 都是执行 clocked(n)
"""
clocked 大致做了下面几件事
1.记录初始时间t0
2.调用原来的 fact 函数,保存结果
3.计算经过的时间
4.格式化收集数据,然后打印出来
5.返回第二步保存的结果
"""
# 这是装饰器的典型行为:把被装饰函数换成新函数,两者接受相同的参数,而且返回被装饰函数本该返回的值,同时执行额外操作
```



## 标准库中的装饰器

```
property	classmethod		staticmethod
functools.wraps		functools.lru_cache		functools.singledispatch
```

### functools.lru_cache

```python
# 优化递归算法,用缓存实现,避免多次调用!
# 必须像常规函数那样调用 lru_cache, 也就是后面那对括号不能少!
import functools
from clockdeco import clock

@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__ == '__main__':
    print(fibonacci(6))
"""
[0.00000060s] fibonacci(0) -> 0
[0.00000050s] fibonacci(1) -> 1
[0.00006040s] fibonacci(2) -> 1
[0.00000100s] fibonacci(3) -> 2
[0.00007980s] fibonacci(4) -> 3
[0.00000070s] fibonacci(5) -> 5
[0.00009920s] fibonacci(6) -> 8
8
"""

# 注意, lru_cache	有两个可选参数, functools.lru_cache(maxsize=128, typed=False)
# maxsize 指定存储多少个调用的结果,缓存满了后旧的结果会被扔掉
# typed 如果设为 True,把不同参数类型得到的结果分开保存,如1和1.0

# 还有一点! lru_cache 使用字典存出结果,键根据调用时传入的参数创建,所以被 lru_cache 装饰的函数,它的所有参数必须是可散列的!
```

### singledispatch

```python
# 单分派泛函数
# 根据参数的类型分配不同的函数处理
from functools import singledispatch
from collections import abc
import numbers
import html

@singledispatch
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)

@htmlize.register(str)
def _(text):
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{}</p>'.format(content)

@htmlize.register(numbers.Integral)
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)

@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

# 取代用一串 if/elif/... 来调用专门的函数
```

### 叠放装饰器

```python
@d1										def f():					
@d2					-- 等价于 -->      		print('f')
def f():								f = d1(d2(f))
    print('f')
```

## 

## 参数化装饰器

```python
# 简单理解:多包装一层
# 为了便于启用或禁用 register 执行的函数注册功能,为它提供一个 active 参数
registry = set()

def register(active=True):
    def decorate(func):
        print('running register(active=%s) -> decorate(%s)'
              % (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate

@register(active=False)
def f1():
    print('running f1()')
```

# 小结

+ functools 中的三个装饰器
+ 区分导入时和运行时
+ 变量作用域, 闭包和 nonlocal 声明