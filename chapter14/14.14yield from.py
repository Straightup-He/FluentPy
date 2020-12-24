"""
yield from
"""
# def chain(*iterables):
#     for it in iterables:
#         for i in it:
#             yield i

def chain(*iterables):
    for i in iterables:
        yield from i

s = 'ABC'
t = tuple(range(3))
print(list(chain(s, t)))  # ['A', 'B', 'C', 0, 1, 2]


