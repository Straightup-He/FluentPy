#-*- coding = utf-8 -*-
#@Time : 2020/12/6 20:19
#@Author : straightup

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