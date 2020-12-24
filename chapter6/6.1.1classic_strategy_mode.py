#-*- coding = utf-8 -*-
#@Time : 2020/12/4 21:11
#@Author : straightup
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

