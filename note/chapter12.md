# 继承的优缺点

**推出继承的初衷是让新手顺利使用只有专家才能设计的框架**

## 子类化内置类型很麻烦

+ 正常情况下, 始终应该从实例所属的类开始搜索方法, 但原生类型不是, 直接子类化内置类型, 内置类型的方法通常会忽略用户覆盖的方法

+ ```python
  # 内置类型 dict 的 __init__ 和 __update__ 方法会忽略我们覆盖的 __setitem__ 方法
  # dict[]	可以执行覆盖方法
  
  class DoppelDict(dict):
      def __setitem__(self, key, value):
          super().__setitem__(key, [value] * 2)
  
  dd = DoppelDict(one=1)
  print(dd)  # {'one': 1}
  
  dd['two'] = 2
  print(dd)  # {'one': 1, 'two': [2, 2]}
  
  dd.update(three=3)
  print(dd)  # {'one': 1, 'two': [2, 2], 'three': 3}
  ```

+ 不直接子类化 dict , 而是子类化 collections.UserDict , 问题就迎刃而解了. 同样的包括 UserList, UserString

  + ```python
    import collections
    
    class DoppelDict2(collections.UserDict):
        def __setitem__(self, key, value):
            super().__setitem__(key, [value] * 2)
    
    ddd = DoppelDict2(one=1)
    print(ddd)  # {'one': [1, 1]}
    
    ddd['two'] = 2
    print(ddd)  # {'one': [1, 1], 'two': [2, 2]}
    
    ddd.update(three=3)
    print(ddd)  # {'one': [1, 1], 'two': [2, 2], 'three': [3, 3]}
    ```

    

## 多重继承

Python 会按照方法解析顺序 (mro) 来遍历继承图

\__mro__ 属性的值是个**元组**, 方法解析顺序使用C3算法计算

搞不清楚继承顺序就用 super() 最安全

### 处理多重继承的建议

+ 区分 **接口继承**(实现'是什么') 和 **实现继承**(重用代码)

+ 抽象基类 显示表示接口

+ 混入类 实现代码重用 (为多个不相关的子类提供方法实现)

  + 混入类应该明确支出 如 ...Mixin

+ 抽象基类可以作为混入类, 反之不成立

+ 不要子类化多个具体类 (不太明白)

+ 聚合类 (将抽象基类和混入类结合起来)

  + ```python
    class Widget(BaseWidget, Pack, Place, Grid):
        """..."""
        pass
    # Widget类的定义体是空的, 但这个类提供了有用的服务:把四个超类结合在一起
    ```

+ 优先使用对象组合, 而不是继承 (组合和委托可以代替混入, 把行为提供给不同的类, 但是不能取代接口继承去定义类型层次结构)

# Django

学习基于类的视图

# 小结

+ 内置类型的原生方法使用C语言实现, 不会调用子类中覆盖的方法, 极少数除外
+ 需要定制 list, dict 或 str 类型时, 子类化 UserList, UserDict 和 UserString 更简单
+ 讨论了多重继承这把双刃剑
  + \__mro__ 属性中蕴藏着继承的顺序
  + super() 函数会按照方法解析顺序调用超类的方法
  + 谨慎使用混入类, 借助组合模式避免多重继承
+ Django 还有很多东西能学习