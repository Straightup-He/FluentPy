#-*- coding = utf-8 -*-
#@Time : 2020/12/26 22:21
#@Author : straightup
import contextlib

@contextlib.contextmanager
def looking_galss():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)

# 测试
with looking_galss() as what:
    print('Alice, Kitty and Snowdrop')  # pordwonS dna yttiK ,ecilA
    print(what)  # YKCOWREBBAJ

print(what)  # JABBERWOCKY

