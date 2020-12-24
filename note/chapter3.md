# 字典

可散列的数据类型 : 原子不可变数据类型(str, bytes, 数值)	frozenset	所有元素都是可散列类型的元组

## 哈希

```
一个对象能被称为 hashable ， 它必须有个 hash 值，这个值在整个生命周期都不会变化，而且必须可以进行相等比较，所以一个对象可哈希，它必须实现__hash__() 与 eq() 方法

对于 Python 的内建类型来说，只要是创建之后无法修改的(immutable)类型都是 hashable 如字符串，可变动的都是 unhashable的比如：列表、字典、集合，他们在改变值的同时却没有改变id,无法由地址定位值的唯一性,因而无法哈希。我们自定义的类的实例对象默认也是可哈希的（hashable），而hash值也就是它们的id()。
总结：一个对象可哈希，必须在其生命周期内通过它的id值确定它的唯一性。
```

## 灵活使用 setdefault 处理找不到的键

```python
my_dict = {}
for i in range(5):
    my_dict.setdefault('key1', []).append(1)
print(my_dict)  # {'key1': [1, 1, 1, 1, 1]}

# 相当于
if 'key1' not in my_dict:
    my_dict['key1'] = []
my_dict['key1'].append(1)

# 返回值:如果字典中包含有给定键，则返回该键对应的值，否则返回为该键设置的值。
```

## defaultdict

```python
import collections
# 如果找不到键,则默认生成一个空列表作为其的值
my_dict = collections.defaultdict(list)

print(my_dict['new_key'])  # []
print(my_dict)  # defaultdict(<class 'list'>, {'new_key': []})

# 如果在创建的时候没有指定default_factory,查询不存在的键则会报KeyError!
# 背后的功臣是__missing__方法!
```

## 其他字典变种

```
collections.OrderedDict		有序字典
collections.Counter			整数计数器(可散列对象计数)
collections.UserDict		子类化字典,如果要继承 Dict 类进行拓展,可以优先考虑继承 UserDict
```

## 不可变映射类型

```python
from types import MappingProxyType

d = {1:'a', 2:'b'}
dd = MappingProxyType(d)

# dd就变为只读的映射类型,不可修改
```

# 集合

许多**唯一对象**的聚集

## 求两个对象的交集

```python
1.set1.intersection(set2,...)

x = {"a", "b", "c"}
y = {"c", "d", "e"}
z = {"f", "g", "c"}
 
result = x.intersection(y, z)
print(result)  # {'c'}

2.set1 & set2
```

# dict 和 set 的背后

## 字典中的散列表

```python
1.首先调用 hash(key) 计算 key 的散列值
2.把这个值最低的几位数字当做偏移量,在散列表中查找表元
3.若查找的表元为空,则返回 KeyError
4.若不为空,则有一对 found_key:value, 然后判断 key == found_key, 为真则返回 value
    为假,则发生散列冲突! 用散列值的另一部分来定位散列表的另一行, 以此循环...
```

## dict 的实现及其导致的结果

```python
1.键必须是可散列的
	支持 hash(); 支持 __eq__() 方法检测相等性; 若a==b,则 hash(a)==hash(b)
2.字典在内存上的巨大开销:散列表的稀疏造成
    存放大量数据,考虑由元组/具名元组构成的列表
3.键查询很快
4.键的次序取决于添加顺序
5.往字典里添加新键可能会改变已有键的顺序:python解释器为字典扩容
    !!!不要对字典同时进行迭代和更新!!!
```

# 小结

+ 字典算得上是python的基石, 除了基本的 Dict 外, 还学习了 defaultdict, OrderedDict, ChainMap, Counter, UserDict
+ setdefault 和 update 两个强大的方法
+ 映射类型中, 有个很好用的方法 \__miss__
+ 字典和集合背后, 散列表效率高的原理