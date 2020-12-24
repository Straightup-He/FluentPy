#-*- coding = utf-8 -*-
#@Time : 2020/12/8 18:08
#@Author : straightup
"""
参数化装饰器
"""
"""
registry = []

def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

print('running main()')
print('registry ->', registry)
f1()

# running register(<function f1 at 0x000001F5F1ECA9D8>)
# running main()
# registry -> [<function f1 at 0x000001F5F1ECA9D8>]
# running f1()
"""

# 为了便于启用或禁用 register 执行的函数注册功能,为它提供一个 active 参数
registry = set()

def register(active=True):
    def decorate(func):
        print('running register(active=%s) -> decorate(%s)'
              % (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate

@register(active=False)
def f1():
    print('running f1()')

@register()
def f2():
    print('running f2()')

def f3():
    print('running f3()')

