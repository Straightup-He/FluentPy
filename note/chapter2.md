# 序列构成的数组



## 容器序列 (容纳多种类型的数据)

```
list	tuple	collections.deque
```



## 扁平序列 (只能容纳一种类型的数据)

```
str		bytes	bytearray	memoryview	 array.array
```



## 可变序列

```
list	bytearray	array.array		collections.deque	  memoryview
```



## 不可变序列

```
tuple	str		bytes
```

# 列表

## 列表生成式

作用只有一个 : 生成列表

笛卡尔积 : 两个或以上的列表中的元素对构成元组, 这些元组构成的列表就是笛卡尔积

## 生成器表达式

作用 : 生成元组和数组等其他类型的序列

# 元组

不仅仅是不可变的列表 !

元组可用作记录, 如记录东京市的信息 (市名, 年份, 人口, 人口变化, 面积)

```python
city, year, pop, chg, area = ('Tokoy', 2003, 32450, 0.6, 8014)

# 元组用做记录信息的时候,其位置就相当重要!
```

# 排序

## list.sort

就地排序列表

## sorted(list) 函数

生成一个新列表

## 共同点

都有 reverse 和 key 两个可选的关键字参数

# bisect

## bisect.bisect

```python
breakpoints = [60, 70, 80, 90]
grades = 'FDCBA'
i = bisect.bisect(breakpoints, score)		# 将score插入breakpoints的索引位置
grades[i]		# 索引对应grades的值就是分数评价
```

## bisect.insort

```python
SIZE = 7
random.seed(1792)

my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    bisect.insort(my_list, new_item)
    print('%2d  ->' % new_item, my_list)
```

# 替换列表的数据结构

## 数组

存放多个浮点数的话, 数组 (array) 的效率要高得多

数组背后存的并不是 float 对象, 而是数字的机器翻译, 也就是字节表述

tofile	fromfile 方法

创建双精度浮点数组 : floats = array ( ' d ' )



## NumPy 和 SciPy

```python
.shape			查看数组的维度
.shape = [x,y]	 改变数组的维度
.transpose		 将数组的行列互换

floats = numpy.loadtxt('.txt')			# 读取文本文件,存到floats数组中
numpy.save('xxx', floats)				# 将floats数组存到.npy的二进制文件中
floats2 = numpy.load('xxx.npy', 'r+')	 # 将.npy文件数据导入floats2数组


```



## 双向队列

双向队列只对头尾的操作做了优化, 但中间删除元素的操作会慢一些

append popleft	先进先出

a_list.pop(n)	这个方法只适用于列表, 双向队列的pop不接收参数

# 小结

+ python序列的分类 : 可变 / 不可变 ; 扁平序列 / 容器序列
  + 扁平序列: 体积更小, 速度更快, 更简单; 但只能保存原子性的数据, 如数字, 字符, 字节
  + 容器序列: 比较灵活, 包含其他对象的引用的对象, 可以嵌套使用 !
+ 列表推导式 和 生成器表达式
+ 元组 : 无名称的字段的记录 / 不可变的列表
  + 拆包	*的用法
  + 具名元组 namedtuple
+ 序列切片
  + 对切片赋值
+ 重复拼接序列 seq * n
  + 增量赋值 += *= 注意可变序列和不可变序列的区别
+ 排序方法 .sort 和 sorted()
  + 都可接收 key 参数(一个函数)
+ 快速查找 bisect.bisect
  + 插入元素还想保持序列的有序性 bisect.insort
+ 除了列表和元组, 还有数组和队列 (collections.deque) 等数据结构
  + array.array
  + NumPy SciPy (扩展)