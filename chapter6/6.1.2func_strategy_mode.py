#-*- coding = utf-8 -*-
#@Time : 2020/12/4 22:14
#@Author : straightup
"""
使用函数实现策略模式
每个策略都是一个函数,省去了抽象基类和定义类
"""
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

# 三种策略
# def fidelity_promo(order):
#     """为积分为1000及以上的顾客提供 5%的折扣"""
#     return order.total() * .05 if order.customer.fidelity >= 1000 else 0
#
# def bulk_item_promo(order):
#     """单个商品数量为20个或以上时提供 10%的折扣"""
#     discount_money = 0
#     for item in order.cart:
#         if item.quantity >= 20:
#             discount_money += item.total() * .1
#     return discount_money
#
# def large_order_promo(order):
#     """订单中的不同商品达到 10个或以上时提供 7%折扣"""
#     distinct_items = {item.product for item in order.cart}
#     return order.total() * .07 if len(distinct_items) >= 10 else 0
#
# 寻找最佳策略的方法
# promos = [fidelity_promo, bulk_item_promo, large_order_promo]
# promos = [globals()[name] for name in globals()
#           if name.endswith('_promo') and name != 'best_promo']
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

# joe_order = Order(joe, cart, fidelity_promo)
# ann_order = Order(ann, cart, fidelity_promo)
# print(joe_order)        # <Order total: 42.00 due: 42.00>
# print(ann_order)        # <Order total: 42.00 due: 39.90>

# 两个客户订单的最大折扣
# print(best_promo(joe_order))  # 0
# print(best_promo(ann_order))  # 2.1

print(Order(joe, cart, best_promo))  # <Order total: 42.00 due: 42.00>
print(Order(ann, cart, best_promo))  # <Order total: 42.00 due: 39.90>



