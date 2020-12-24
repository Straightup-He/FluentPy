"""
生成器函数
"""
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end')


for item in gen_AB():
    print('>>>', item)
"""
start
>>> A
continue
>>> B
end
"""