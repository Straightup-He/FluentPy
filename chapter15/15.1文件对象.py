with open('test', encoding='utf-8') as fp:
    src = fp.read(60)

print(len(src))   # 60
print(fp)         # <_io.TextIOWrapper name='test' mode='r' encoding='utf-8'>
print(fp.closed, fp.encoding)  # True utf-8
print(fp.read(60))  # 报错 ValueError: I/O operation on closed file.
