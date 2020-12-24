"""
itertools  aritprog_gen
"""
import itertools

def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen

"""
注意：aritprog_gen 不是生成器函数，因为定义体中没有 yield 关键字。但是它会返回一个生成器，因此它与其他生成器函数一样，也是生成器工厂函数！
"""