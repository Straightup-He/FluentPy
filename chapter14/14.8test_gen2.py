"""
生成器表达式
"""
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end')

res1 = [x*3 for x in gen_AB()]
for i in res1:
    print('-->', i)
"""
start
continue
end
--> AAA
--> BBB
"""
# 列表推导式则迫切地迭代gen_AB()函数生成的生成器对象产出的元素

res2 = (x*3 for x in gen_AB())
for i in res2:
    print('-->', i)
"""
start
--> AAA
continue
--> BBB
end
"""
# 夹杂在一起
# for循环的时候，gen_AB()函数的定义体才执行
