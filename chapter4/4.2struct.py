#-*- coding = utf-8 -*-
#@Time : 2020/12/2 22:02
#@Author : straightup
"""
struct模块处理二进制文件
"""
# 使用 struct 和 memoryview 查看图像的宽度和高度
import struct
fmt = '<3s3sHH'  # 结构体的格式
with open('1.jpg', 'rb') as fp:
    img = memoryview(fp.read())

header = img[:10]
print(bytes(header))  # b'\xff\xd8\xff\xe0\x00\x10JFIF'

# print(struct.unpack(fmt, header))
# (b'\xff\xd8\xff', b'\xe0\x00\x10', 17994, 17993)
width, height = struct.unpack(fmt, header)[-2:]
print(width, height)  # 17994 17993

del header
del img


