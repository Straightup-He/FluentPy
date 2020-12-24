"""
有穷等差数列
"""
class ArithmeticProgression:

    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end  # None -> 无穷数列

    def __iter__(self):
        # 行把 self.begin 赋值给 result，不过会先强制转换成前面的加法算式得到的类型
        result = type(self.begin + self.step)(self.begin)
        forever = self.end is None  # bool
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index


