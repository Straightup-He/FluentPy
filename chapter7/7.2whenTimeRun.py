#-*- coding = utf-8 -*-
#@Time : 2020/12/6 23:03
#@Author : straightup
"""
装饰器何时执行
"""
registry = []

def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

@register
def f2():
    print('running f2()')


def f3():
    print('running f3()')

def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()

if __name__ == '__main__':
    main()

"""
作为脚本运行:
running register(<function f1 at 0x00000181349FA9D8>)
running register(<function f2 at 0x0000018134BCC2F0>)
running main()
registry -> [<function f1 at 0x00000181349FA9D8>, <function f2 at 0x0000018134BCC2F0>]
running f1()
running f2()
running f3()
"""

