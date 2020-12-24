# 上下文管理器和 else 块

## else块

else 子句不仅能在 if 语句中使用, 还能在 for , while, try 语句中使用

try - else : 当 try 块中没有抛出异常时才运行 else 块 ( else 子句抛出的异常不会由前面的 except 子句处理 ! )

try - except - else : 不仅英语处理错误, 还常用于控制流程

## 上下文管理器和with块

上下文管理器对象存在的目的是管理 with 语句，就像迭代器的存在是 为了管理 for 语句一样。

with语句的目的：是简化 try/finally 模式，用于保证一段代 码运行完毕后执行某项操作（中途中止也会执行！）

上下文管理器协议包含 __enter__ 和 __exit__ 两个方法（with 语句开始运行时，会在上下文管理器对象上调用 __enter__ 方法。with 语句运行结束后，会在上下文管理器对象上调用 __exit__ 方法，以此扮演 finally 子句的角色。）

### 把文件对象当成上下文管理器使用

```python
with open('test', encoding='utf-8') as fp:
    src = fp.read(60)

print(len(src))   # 60
print(fp)         # <_io.TextIOWrapper name='test' mode='r' encoding='utf-8'>  上下文管理器对象
print(fp.closed, fp.encoding)  # True utf-8
print(fp.read(60))  # 报错 ValueError: I/O operation on closed file.

# with块后 fp 变量仍然可用，可以读取 fp 对象的属性
#  但是不能在 fp 上执行 I/O 操作，因为在 with 块的末尾，调用TextIOWrapper.__exit__ 方法把文件关闭了
```

**不管控制流程以哪种方式退出 with 块，都会在上下文管理器对象上调用 exit 方法，而不是在 enter 方法返回的对象上调用。**

LookingGlass 上下文管理器类的代码

```python
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
```

传给 __exit__ 方法的三个参数:

+ 异常类	    exc_type
+ 异常实例    exc_value
+ traceback对象

```python
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
```

