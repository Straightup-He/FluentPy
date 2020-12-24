#-*- coding = utf-8 -*-
#@Time : 2020/12/7 22:04
#@Author : straightup

import time
from clockdeco import clock

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)


if __name__ == '__main__':
    print('*'*40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))

"""
**************************************** Calling snooze(.123)
[0.13334950s] snooze(0.123) -> None
**************************************** Calling factorial(6)
[0.00000280s] factorial(1) -> 1
[0.00006780s] factorial(2) -> 2
[0.00011840s] factorial(3) -> 6
[0.00016270s] factorial(4) -> 24
[0.00020720s] factorial(5) -> 120
[0.00025660s] factorial(6) -> 720
6! = 720
"""
