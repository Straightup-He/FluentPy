# 符合Python风格的对象

**鸭子类型 : 我们只需按照预定行为==实现对象所需要的方法==即可**

## 对象的表示形式

python提供了两种形式

+ repr()     以便于**开发者**理解的方式返回对象的字符串表示形式
+ str()        以便于**用户**理解的方式返回对象的字符串表示形式



## 创建可散列的类型

只需正确地实现 \__\_hash__ 和  \_\_eq__ 方法即可, 但是实例的散列值绝对不能变化 (只读特性)



## Python 的私有属性和"受保护的"属性

==避免子类意外覆盖"私有"属性==

+ 使用一个下划线前缀标记的属性称为 "受保护的" 属性
  + 解释器不会做特殊处理, 只是大家严格遵守的约定而已
+ 使用两个下划线前缀标记的属性称为**私有**属性
  + \__x (内部)            _类名__x (外部调用)

# 小结

+ 本章目的 : 如何使用特殊方法和约定的结构, 定义行为良好且符合 Python 风格的类

+ 简洁胜于复杂, 符合所需即可, 无需堆砌语言特性

+ ```python
  所有用于获取字符串和字节序列表示形式的方法: __repr__, __str__, __format__, __bytes__
  把对象转换成数字的几个方法: __abs__, __bool__, __hash__
  用于测试字节序列转换和支持散列(__hash__) __eq__ 运算符
  ```

+ @classmethod 和 @staticmethod

+ \__slots__ 属性节省内存

+ 通过访问类属性来覆盖类属性