"""
LookingGlass 上下文管理器类的代码
"""
class LookingGlass:
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write  # 猴子补丁
        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, traceback):
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True


# 测试
with LookingGlass() as what:
    print('Alice, Kitty and Snowdrop')
    print(what)
"""
pordwonS dna yttiK ,ecilA
YKCOWREBBAJ
"""
print(what)  # JABBERWOCKY


# --------------- 在with块以外的地方测试 ---------------
# 实例化并审查 manager 实例
manager = LookingGlass()
print(manager)   # <__main__.LookingGlass object at 0x00000000020C24A8>

# 在上下文管理器上调用 __enter__() 方法
monster = manager.__enter__()
print(monster == 'JABBERWOCKY')  # eurT
print(monster)                   # YKCOWREBBAJ
print(manager)    # >0D16302000000000x0 ta tcejbo ssalGgnikooL.__niam__<

# 调用 manager.__exit__，还原成之前的 stdout.write
manager.__exit__(None, None, None)
print(monster)    # JABBERWOCKY
