# 把函数视作对象

+ 函数可以赋值给变量
+ 函数可以作为参数传递

## 高阶函数

接收函数为参数, 或者把函数作为结果返回的函数是高阶函数

## map, filter, reduce 的替代品

+ 列表推导式 取代 map, filter
+ 生成器推导式 取代 map+filter
+ 归约函数 取代 reduce
  + sum, all, any

## 匿名函数

除了作为参数传给高阶函数, 其余地方很少用到匿名函数

由于句法限制, 要么难读要么无法写出

## 可调用对象

除了用户定义的函数, ()调用运算符还可以应用到其他对象上, 可以用 callable() 函数判断对象是否可调用

```shell
1.用户定义的函数 由def或lambda表达式创建
2.内置函数	如len
3.内置方法	如dict.get
4.方法	在类的定义体中定义的函数
5.类
	调用类会运行类的__new__方法生成实例,然后运行__init__方法进行初始化,最后把实例返回给调用方
6.类的实例
	如果类定义了__call__方法,那么它的实例可以作为函数调用
7.生成器函数(?)
	使用yield关键字的函数或方法,调用生成器函数返回的是生成器对象
```

## 支持函数式编程的包

### operator模块

```python
"""
# 使用reduce函数和一个匿名函数计算阶乘
from functools import reduce

def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))
"""
# 使用reduce和operator.mul函数计算阶乘
from functools import reduce
from operator import mul

def fact(n):
    return reduce(mul, range(1, n+1))
```

```
itemgetter, attrgetter	看的不是很明白
```

```python
# methodcaller 自行创建函数
from operator import methodcaller

s = 'Winter is coming!'
upcase = methodcaller('upper')
print(upcase(s))  # WINTER IS COMING!
"""
upcase = methodcaller('uupper')
print(upcase(s))  # 报错 AttributeError: 'str' object has no attribute 'urpper'
"""

# methodcaller 也可以冻结某些参数(replace需要两个参数, 而my_replace只需传入一个)
my_replace = methodcaller('replace', ' ', '-')
print(my_replace(s))  # Winter-is-coming!
print(s.replace(' ', '-'))  # Winter-is-coming!
```

### functools.partial

```python
# 同样可以冻结参数的 functools.partial
from operator import mul
from functools import partial

triple = partial(mul, 3)
print(triple(7))    # 21
print(list(map(triple, range(1, 6))))  # [3, 6, 9, 12, 15]
```

# 小结

+ 探讨 python 函数的一等本性, 即可以把函数赋值给变量, 传给其他函数, 存储在数据结构中, 以及访问函数的属性等...
+ 高阶函数 map, filter, reduce, sorted, min, max...
+ python 的 7 种可调用对象 (从 lambda 表达式创建的简单函数到实现 \__call__ 方法的类实例对象)
+ 函数的传参
+ python 函数的注解和参数属性
+ 还有了解了 operator 和 functools 模块的一些函数