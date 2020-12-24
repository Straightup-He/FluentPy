# 对象引用, 可变性

**变量是标注而不是盒子 !**



## 标识, 相等性和别名

每个变量都有标识, 类型和值. 对象一旦创建, 它的标识就不会改变(内存地址). is 比较两个对象的标识, id()函数返回对象标识的整数表示

### is 和 ==

```
is 比 == 速度更快,因为其不能重载, python不用寻找并调用特殊方法
a == b 是语法糖, 相当于 a.__eq__(b)
```

### 数据结构

```
str, bytes, array.array 等单一类型序列是扁平的. 它们保存的不是引用, 而是在连续的内存中保存数据本身
元组, 列表, 字典, 集合等, 保存的是对象的引用
```



## 默认做浅复制

### 列表复制

```
l1 = [3,  [55,44], (7,8,9)]
l2 = list(l1)

l2 = l1[:]
```

### 浅拷贝

```python
l1 = [3, [66, 55], (7, 8)]
l2 = list(l1)
l1[1].remove(55)
print(l1)  # [3, [66], (7, 8)]
print(l2)  # [3, [66], (7, 8)]
l2[1] += [22, 33]
l2[2] += (10, 11)
print(l1)  # [3, [66, 22, 33], (7, 8)]
print(l2)  # [3, [66, 22, 33], (7, 8, 10, 11)]

# 列表+=就地改变; 元组+=生成新元组
l1 = [1, 2, 3]
print(id(l1))  # 2855995581256
l1 += [1, 2, 3]
print(id(l1))  # 2855995581256

t2 = (1, 2, 3)
print(id(t2))  # 2855996394304
t2 += (4, 5)
print(l1, t2)  # [1, 2, 3, 1, 2, 3] (1, 2, 3, 4, 5)
print(id(t2))  # 2855998244472


# 浅拷贝也是多生成了一份,只是里面的元素是共用的
lst = [1, 2, 3]
lst2 = list(lst)
lst.append(4)
print(lst, lst2)  # [1, 2, 3, 4] [1, 2, 3]
print(id(lst), id(lst2))  # 2198258333768 2198258444040
```

### 深拷贝

```python
import copy

class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

bus1 = Bus(["Alice", "Bill", "Claire", "David"])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)
print(id(bus1), id(bus2), id(bus3))
# 2476561331424 2476561330640 2476561376760

# Bill下车
bus1.drop('Bill')
print(bus2.passengers)  # ['Alice', 'Claire', 'David']
print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))
# 2285356641352 2285356641352 2285356565960
# bus1 和 bus2 的乘客id是一样的
print(bus3.passengers)  # ['Alice', 'Bill', 'Claire', 'David']

# 循环引用 进入无限循环
a = [10, 20]
b = [a, 30]
a.append(b)
print(a)  # [10, 20, [[...], 30]]
c = copy.deepcopy(a)
print(c)  # [10, 20, [[...], 30]]
```



## 函数的参数作为引用时

```python
"""
函数的参数作为引用时
"""
def f(a, b):
    a += b
    return a

x = 1
y = 2
f(x, y)
print(x, y)  # 1 2  不变

a = [1, 2]
b = [3, 4]
f(a, b)
print(a, b)  # [1, 2, 3, 4] [3, 4]  a发生改变!

t1 = (10, 20)
t2 = (30, 40)
f(t1, t2)
print(t1, t2)  # (10, 20) (30, 40)  元组不变

# python唯一支持的参数传递模式是 共享传参 
# 共享传参:指函数的 各个形参 获得 实参中各个引用 的副本. 也就是说函数内部的形参是实参的别名
# 这样导致的结果:函数可能会修改作为参数传入的可变对象,但无法修改那些对象的标识
	# 就像上面, a对应的列表对象已经修改了, 但标识还是a
```



## 防御可变参数

除非这个方法确实想修改通过参数传入的对象, 否则在类中直接把参数赋值给实例变量前一定要三思 ! 因为这样会为参数创建别名, 如果不确定, 那就创建副本(拷贝). 

# del 和 垃圾回收

**对象绝不会自行销毁, 然而, 无法得到对象的时候, 可能会被当做垃圾回收**

+ del 删除的是名称, 而不是对象!
+ 仅当删除的变量指向的是对象的最后一个引用, 或无法得到对象时(==最后一个引用改变了==), del 命令才可能导致对象被当做垃圾来回收
+ 两个对象互相引用也可能会被程序判定均无法获取而被销毁

```python
import weakref
s1 = {1, 2, 3}
s2 = s1
def bye():
    print('Gone with the wind...')

ender = weakref.finalize(s1, bye)
print(ender.alive)  # True
del s1
print(ender.alive)  # True
# 重新绑定s2的指向
s2 = 'Spam'
# Gone with the wind...
print(ender.alive)  # False
```



## 弱引用

**弱引用在缓存应用中很有用, 因为我们不想仅因为被缓存引用而始终保存缓存对象**

```python
"""
WeakValueDictionary
是一个类,实现的是一种可变映射,里面的值是对象的弱引用
被引用的对象在程序的其他地方被当做垃圾回收以后,对应的键会自动从中删除
因此其经常用于缓存
"""
class Cheese:
    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return 'Cheese(%r)' % self.kind

import weakref

stock = weakref.WeakValueDictionary()

catalog = [Cheese('Red Leicester'), Cheese('Tilsit'), Cheese('Brie'), Cheese('Parmesan')]
for cheese in catalog:
    stock[cheese.kind] = cheese

print(sorted(stock.keys()))  # ['Brie', 'Parmesan', 'Red Leicester', 'Tilsit']
del catalog
print(sorted(stock.keys()))  # ['Parmesan']  cheese是全局变量!引用了Parmesan
del cheese
print(sorted(stock.keys()))  # []
```

+ WeakValueDictionary		值是弱引用
+ WeakKeyDictionary           键是弱引用
+ WeakSet                            保存元素弱引用的集合类

# 小结

+ 每个 Python 对象都有==标识, 类型和值==, 其中只有值可能会变化
+ **变量保存的是对象的引用**
  + 简单的赋值不创建副本
  + += 和 *= 这样的增量赋值, 如果左边的变量绑定的是不可变对象, 会创建新对象; 如果是可变对象, 则就地修改
  + 为现有的变量赋予新值, 不会修改之前绑定的变量. 这叫重新绑定 . 如果变量是之前那个对象的最后一个引用, 对象就会被当做垃圾回收
  + 函数的参数以别名形式传递, 这意味着函数可能会修改通过参数传入的可变对象
  + 使用可变类型作为函数的默认参数很危险 !
+ 引用计数, 循环引用
+ 某些情况可能需要保存对象的引用, 而不保存对象本身, 则可以使用弱引用实现
  + weakref 模块的三个类