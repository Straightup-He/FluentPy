# 使用期物处理并发

“期物”（future） 的概念。期物指一种对象，表示异步执行的操作。这个概念的作用很大，是 concurrent.futures 模块和 asyncio 包的基础。

依序下载的脚本：

```python
import os
import time
import sys

import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'http://flupy.org/data/flags'

DEST_DIR = 'downloads/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')
    return len(cc_list)


def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
```

使用concurrent.futures模块下载：

```python
from concurrent import futures

from flags import save_flag, get_flag, show, main

MAX_WORKERS = 20


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))  # 避免创建过多线程
    # download_one 函数会在多个线程中并发调用
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))  # map方法返回一个生成器
    return len(list(res))


if __name__ == '__main__':
    main(download_many)

# download_one 函数其实是 flag.py 中 download_many 函数的 for 循环体。编写并发代码时经常这样重构：把依序执行的 for 循环体改成函数，以便并发调用
```

使用concurrent.futures模块下载（用 submit 和 as_completed 函数替换 map 函数）：

```python
from concurrent import futures

from flags import save_flag, get_flag, show, main

MAX_WORKERS = 20


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            # executor.submit 方法可以排定可调用对象的执行时间，然后返回一个future，表示这个待执行的操作
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))
        
        results = []
        # as_completed 函数在future运行结束后产出future
        for future in futures.as_completed(to_do):
            # result 方法获取该future的结果
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)
    
    return len(results)


if __name__ == '__main__':
    main(download_many)

```

































