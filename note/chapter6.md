# 使用一等函数实现设计模式

## 经典的 "策略" 模式

```
定义一系列算法,把它们一一封装起来,并且使它们可以相互替换.本模式使得算法可以独立于使用它的客户而变化
```

```python
"""
经典的策略模式
"""
# 实现Oder类,支持插入式折扣策略
from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')  # 客户名和积分

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

# 上下文
class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

# 定义策略(抽象基类)
class Promotion(ABC):
    @abstractmethod
    def discount(self, order):
        """返回折扣金额(正值)"""

# 第一个具体策略
class FidelityPromo(Promotion):
    """为积分为1000及以上的顾客提供 5%的折扣"""
    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0

# 第二个具体策略
class BulkItemPromo(Promotion):
    """单个商品数量为20个或以上时提供 10%的折扣"""
    def discount(self, order):
        discount_money = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount_money += item.total() * .1
        return discount_money

# 第三个策略
class LargeOrderPromo(Promotion):
    """订单中的不同商品达到 10个或以上时提供 7%折扣"""
    def discount(self, order):
        # 将产品放到集合中去重
        distinct_items = {item.product for item in order.cart}
        return order.total() * .07 if len(distinct_items) >= 10 else 0

"""
测试用例
"""
# 两个客户
joe = Customer('John', 0)
ann = Customer('Ann', 1100)
# 购物车
cart = [LineItem('banana', 4, 0.5),
        LineItem('apple', 10, 1.5),
        LineItem('watermellon', 5, 5.0)]

# 两个客户的订单情况(使用 FidelityPromo 策略)
joe_order = Order(joe, cart, FidelityPromo())
print(joe_order)  # <Order total: 42.00 due: 42.00>

ann_order = Order(ann, cart, FidelityPromo())
print(ann_order)  # <Order total: 42.00 due: 39.90>

# 两个客户的订单情况(使用 BulkItemPromo 策略)
# 很多香蕉的购物车
banana_cart = [LineItem('banana', 30, 0.5),
               LineItem('apple', 10, 1.5)]
joe_order = Order(joe, banana_cart, BulkItemPromo())
print(joe_order)  # <Order total: 30.00 due: 28.50>

ann_order = Order(ann, banana_cart, BulkItemPromo())
print(ann_order)  # <Order total: 30.00 due: 28.50>
```



## 使用函数实现 "策略" 模式

```python
"""
使用函数实现策略模式
每个策略都是一个函数,省去了抽象基类和定义类
"""
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

# 单种商品
class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

# 订单情况
class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

# 三种策略
def fidelity_promo(order):
    """为积分为1000及以上的顾客提供 5%的折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

def bulk_item_promo(order):
    """单个商品数量为20个或以上时提供 10%的折扣"""
    discount_money = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount_money += item.total() * .1
    return discount_money

def large_order_promo(order):
    """订单中的不同商品达到 10个或以上时提供 7%折扣"""
    distinct_items = {item.product for item in order.cart}
    return order.total() * .07 if len(distinct_items) >= 10 else 0

# 寻找最佳策略的方法
promos = [fidelity_promo, bulk_item_promo, large_order_promo]
def best_promo(order):
    """选用可用的最佳折扣"""
    return max(promo(order) for promo in promos)

# 定义两个用户
joe = Customer('John', 0)
ann = Customer('Ann', 1100)
# 一个购物车
cart = [LineItem('banana', 4, 0.5),
        LineItem('apple', 10, 1.5),
        LineItem('watermellon', 5, 5.0)]

joe_order = Order(joe, cart, fidelity_promo)
ann_order = Order(ann, cart, fidelity_promo)
# print(joe_order)        # <Order total: 42.00 due: 42.00>
# print(ann_order)        # <Order total: 42.00 due: 39.90>

# 两个客户订单的最大折扣
print(best_promo(joe_order))  # 0
print(best_promo(ann_order))  # 2.1

print(Order(joe, cart, best_promo))  # <Order total: 42.00 due: 42.00>
print(Order(ann, cart, best_promo))  # <Order total: 42.00 due: 39.90>
```



## 寻找全部策略的方法

+ 列表装载（最简单，但是可扩展性差）

```
promos = [fidelity_promo, bulk_item_promo, large_order_promo]
```

+ globals()

```python
promos = [globals()[name] for name in globals()
          if name.endswith('_promo') and name != 'best_promo']
#globals()，返回一个字典，表示当前的全局符号表。这个符号表始终针对当前模块
#里面包括了定义的函数（见最后几个）

print(globals())
"""
{'__name__': '__main__', '__doc__': '\n使用函数实现策略模式\n每个策略都是一个函数,省去了抽象基类和定义类\n', '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x0000025689E21CF8>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': 'C:/Users/harris/Desktop/fluentPy/chapter6/6.1.2func_strategy_mode.py', '__cached__': None, 'inspect': <module 'inspect' from 'C:\\Users\\harris\\AppData\\Local\\Programs\\Python\\Python37\\lib\\inspect.py'>, 'promotions': <module 'promotions' from 'C:\\Users\\harris\\Desktop\\fluentPy\\chapter6\\promotions.py'>, 'namedtuple': <function namedtuple at 0x000002568BC45EA0>, 'Customer': <class '__main__.Customer'>, 'LineItem': <class '__main__.LineItem'>, 'Order': <class '__main__.Order'>, 'fidelity_promo': <function fidelity_promo at 0x000002568BD2F730>, 'bulk_item_promo': <function bulk_item_promo at 0x000002568BD2FAE8>, 'large_order_promo': <function large_order_promo at 0x000002568BD2FB70>, 'promos': [<function bulk_item_promo at 0x000002568BD2F378>, <function fidelity_promo at 0x000002568BD2F2F0>, <function large_order_promo at 0x000002568BD2F400>], 'best_promo': <function best_promo at 0x000002568BD2FBF8>}
"""
```

+ 内省模块 + 提供高阶内省函数的模块 inspect

```python
promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]

# inspect.getmembers 函数用于获取promotions模块的属性，第二个参数是可选的判断条件，我们这里选择获取模块中的函数（inspect.isfunction）
```

### 完整代码

```python
# promotions.py
# 单独存放所有策略函数

def fidelity_promo(order):
    """为积分为1000及以上的顾客提供 5%的折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

def bulk_item_promo(order):
    """单个商品数量为20个或以上时提供 10%的折扣"""
    discount_money = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount_money += item.total() * .1
    return discount_money

def large_order_promo(order):
    """订单中的不同商品达到 10个或以上时提供 7%折扣"""
    distinct_items = {item.product for item in order.cart}
    return order.total() * .07 if len(distinct_items) >= 10 else 0
```

```python
# 主模块

import inspect
import promotions

from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

# 单种商品
class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

# 订单情况
class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

# 寻找最佳策略的方法
promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]
def best_promo(order):
    """选用可用的最佳折扣"""
    return max(promo(order) for promo in promos)
print(globals())

# 定义两个用户
joe = Customer('John', 0)
ann = Customer('Ann', 1100)
# 一个购物车
cart = [LineItem('banana', 4, 0.5),
        LineItem('apple', 10, 1.5),
        LineItem('watermellon', 5, 5.0)]
# 用户最佳策略
print(Order(joe, cart, best_promo))  # <Order total: 42.00 due: 42.00>
print(Order(ann, cart, best_promo))  # <Order total: 42.00 due: 39.90>
```

## 

## 命令模式

看不懂，先放一放

# 小结

+ "命令模式" 和 "策略模式" 都可以使用一等函数实现