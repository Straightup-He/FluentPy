#-*- coding = utf-8 -*-
#@Time : 2020/11/30 22:15
#@Author : straightup

import collections

# 借助namedtuple生成一个类,来表示一张纸牌
# 适用于构建只有少数属性且没有方法的对象
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDesk(object):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()  # 默认以空格切割

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


# 得到一张纸牌
beer_card = Card('7', 'spades')
print(beer_card)  # Card(rank='7', suit='spades')

# 重点还是FrenchDesk
deck = FrenchDesk()
print(len(deck))    # 52

# 抽取第一张和最后一张纸牌
print(deck[0], deck[-1])
# Card(rank='2', suit='spades') Card(rank='A', suit='hearts')

# ------------------------  试下随机抽取一张纸牌  ------------------------
from random import choice

print(choice(deck))  # Card(rank='6', suit='hearts')
print(choice(deck))  # Card(rank='2', suit='spades')

# ------------------------  好戏开始了  ------------------------
# 由于实现了__getitem__方法,所以支持切片!
# 查看牌堆顶部的三张牌(顾前不顾后)
print(deck[:3])
# [Card(rank='2', suit='spades'), Card(rank='3', suit='spades'), Card(rank='4', suit='spades')]

# 只看牌面是A的牌
print(deck[12])  # Card(rank='A', suit='spades')
# 第十二张牌是第一张A,之后每隔13张拿一张
print(deck[12::13])
# [Card(rank='A', suit='spades'), Card(rank='A', suit='diamonds'), Card(rank='A', suit='clubs'), Card(rank='A', suit='hearts')]

# 另外,实现了__getitem__方法,deck变得可迭代了!
# for card in deck:
#     print(card)

# 反向迭代
# for card in reversed(deck):
#     print(card)

# 由于可迭代,in运算符也可以用在我们的 deck上
print(Card('Q', 'diamonds') in deck)  # True

# ------------------------  排序  ------------------------
# 规则: 点数2最小 A最大; 花色 spades > hearts > diamonds > clubs
suit_values = dict(spades=3, hearts=2, diamonds=3, clubs=4)
print(suit_values)  # {'spades': 3, 'hearts': 2, 'diamonds': 3, 'clubs': 4}

def spades_high(card):
    # JQKA不是数字,无法像 2-10 一样进行乘法运算,用它们对应的索引来代替
    rank_value = FrenchDesk.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

# 借助 spades_high 函数排序
# sorted 会返回一个新的排好序的列表
# for card in sorted(deck, key=spades_high):
#     print(card)

# 如何洗牌 ? 目前不能实现,因为这副牌是不可变的,但其实只需要定义__setitem__方法即可.
