"""
Sentence类第一版：单词序列
"""
import re
from collections import abc
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        """用于生成大型数据结构的简略字符串表示形式
        reprlib.repr默认生成30个字符"""
        return 'Sentence(%s)' % reprlib.repr(self.text)

    # def __iter__(self):
    #     pass


# 测试Sentence实例可否迭代
s = Sentence('"The time has come," the Walrus said,')
print(s)  # Sentence('"The time ha... Walrus said,')

for word in s:
    print(word)
"""
The
time
has
come
the
Walrus
said
"""
print(list(s))  # ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']

print(issubclass(Sentence, abc.Iterable))  # False
print(isinstance(s, abc.Iterable))  # False
print(iter(s))  # <iterator object at 0x0000000002581278>

# 构建迭代器
s3 = Sentence('Pig and Pepper')
it = iter(s3)
print(it)    # <iterator object at 0x00000000025614E0>
print(next(it))  # Pig
print(next(it))  # and
print(next(it))  # Pepper
print(next(it))  # 抛出异常 StopIteration

