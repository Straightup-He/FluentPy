#-*- coding = utf-8 -*-
#@Time : 2020/12/2 16:38
#@Author : straightup

# s = {1}
# print(type(s))

# 字节码判断{1,2,3}这种构造集合的方法效率更高
from dis import dis

# dis('{1}')
"""
  1           0 LOAD_CONST               0 (1)
              2 BUILD_SET                1
              4 RETURN_VALUE
"""
# dis('set([1])')
"""
  1           0 LOAD_NAME                0 (set)
              2 LOAD_CONST               0 (1)
              4 BUILD_LIST               1
              6 CALL_FUNCTION            1
              8 RETURN_VALUE
"""

# 但是 frozenset 没有这种字面量句法...
print(frozenset(range(10)))
# frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9})

# ---------------- 集合推导 ---------------------
print({i for i in range(20) if i % 2 == 0})
# {0, 2, 4, 6, 8, 10, 12, 14, 16, 18}





